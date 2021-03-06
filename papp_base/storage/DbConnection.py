"""
 *  Copyright Synerty Pty Ltd 2016
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by
 *  Synerty Pty Ltd
 *
"""
import logging
from tempfile import NamedTemporaryFile
from textwrap import dedent
from threading import Lock
from time import sleep

import sqlalchemy_utils
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import Sequence, MetaData

logger = logging.getLogger(__name__)


class DbConnection:
    def __init__(self, dbConnectString: str, metadata: MetaData, alembicDir: str,
                 dbEngineArgs: {} = None,
                 enableForeignKeys=False, enableCreateAll=True):
        """ SQLAlchemy Database Connection

        This class takes care of migrating the database and establishing thing database
        connections and ORM sessions.

        :param dbConnectString:
            The connection string for the DB.
            See http://docs.sqlalchemy.org/en/latest/core/engines.html

        :param metadata:
            The instance of the metadata for this connection,
            This is schema qualified MetaData(schema="schama_name")

        :param alembicDir:
            The absolute location of the alembic directory (versions dir lives under this)

        :param dbEngineArgs:
            The arguments to pass to the database engine, See
            http://docs.sqlalchemy.org/en/latest/core/engines.html#engine-creation-api

        :param enableCreateAll:
            If the schema doesn't exist, then the migration is allowed
            to use matadata.create_all()

        :param enableForeignKeys:
            Perform a check to ensure foriegn keys have indexes after the db is
            migrated and connected.
        """
        self._dbConnectString = dbConnectString
        self._metadata = metadata
        self._alembicDir = alembicDir

        self._dbEngine = None
        self._ScopedSession = None
        self._dbEngineArgs = dbEngineArgs if dbEngineArgs else {"echo": False}

        self._sequenceMutex = Lock()

        self._enableForeignKeys = enableForeignKeys
        self._enableCreateAll = enableCreateAll

    def closeAllSessions(self):
        """ Close All Session

        Close all ORM sessions connected to this DB engine.

        """
        self.ormSession()  # Ensure we have a session maker
        self._ScopedSession.close_all()

    @property
    def ormSession(self) -> Session:
        """ Get Orm Session

        :return: A SQLAlchemy session scoped for the callers thread..
        """
        assert self._dbConnectString

        if self._ScopedSession:
            return self._ScopedSession()

        self._dbEngine = create_engine(
            self._dbConnectString,
            **self._dbEngineArgs
        )

        self._ScopedSession = scoped_session(
            sessionmaker(bind=self._dbEngine))

        return self._ScopedSession()

    @property
    def dbEngine(self) -> Engine:
        """ Get DB Engine

        This is not thread safe, use the ormSesson to execute SQL statements instead.
        self.ormSession.execute(...)

        :return: the DB Engine used to connect to the database.

        """
        return self._dbEngine

    def migrate(self) -> None:
        """ Migrate

        Perform a database migration, upgrading to the latest schema level.
        """

        assert self.ormSession

        isDbInitialised = self._dbEngine.dialect.has_table(
            self._dbEngine.connect(), 'alembic_version',
            schema=self._metadata.schema)

        if isDbInitialised or not self._enableCreateAll:
            self._doMigration(self._dbEngine)

        else:
            self._doCreateAll(self._dbEngine)

        if self._enableForeignKeys:
            self.checkForeignKeys(self._dbEngine)

    def checkForeignKeys(self, engine: Engine) -> None:
        """ Check Foreign Keys

        Log any foreign keys that don't have indexes assigned to them.
        This is a performance issue.

        """
        missing = (sqlalchemy_utils.functions
                   .non_indexed_foreign_keys(self._metadata, engine=engine))

        for table, keys in missing.items():
            for key in keys:
                logger.warning("Missing index on ForeignKey %s" % key.columns)

    def getPgSequenceGenerator(self, Declarative, count):
        """ Get Postgresql Sequence Generator

        :return: A generator that yields each ID up to (count) more than the current
                    latest DB id.
        """
        if not count:
            return

        session = self.ormSession
        session.commit()

        while not self._sequenceMutex.aquire():
            sleep(0.001)

        # Something about the backend not updating curval/nextval causes issues when
        #
        sequence = Sequence('%s_id_seq' % Declarative.__tablename__)
        startId = session.execute(sequence) + 1
        endId = startId + count

        session.execute('alter sequence "%s" restart with %s'
                        % (sequence.name, endId + 1))
        session.commit()

        self._sequenceMutex.release()

        while startId < endId:
            yield startId
            startId += 1

    def _runAlembicCommand(self, command, *args):
        configFile = self._writeAlembicIni()

        from alembic.config import Config
        alembic_cfg = Config(configFile.name)
        command(alembic_cfg, *args)

    def _doCreateAll(self, engine):

        self._dbEngine.execute('CREATE SCHEMA IF NOT EXISTS "%s" '
                               % self._metadata.schema)
        self._metadata.create_all(self._dbEngine)

        from alembic import command
        self._runAlembicCommand(command.stamp, "head")

    def _writeAlembicIni(self):
        cfg = '''
        [alembic]
        script_location = %(alembicDir)s
        sourceless = true
        sqlalchemy.url = %(url)s

        [alembic:exclude]
        tables = spatial_ref_sys

        [logging]
        default_level = INFO
        '''
        cfg = dedent(cfg)

        cfg %= {'alembicDir': self._alembicDir,
                'url': self._dbConnectString}

        tempFile = NamedTemporaryFile('w+t')
        tempFile.write(cfg)
        tempFile.flush()
        return tempFile

    def _doMigration(self, engine):
        from alembic import command
        self._runAlembicCommand(command.upgrade, "head")
