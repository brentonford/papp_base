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

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import Sequence

logger = logging.getLogger(__name__)


class DbConnBase:
    def __init__(self, dbConnectString, metadata, alembicDir):
        self._dbConnectString = dbConnectString
        self._metadata = metadata
        self._alembicDir = alembicDir

        self._dbEngine = None
        self._ScopedSession = None
        self._dbEngineArgs = {"echo": False}

        self._sequenceMutex = Lock()

        self._enableCreateAll = True

    def closeAllSessions(self):
        self.getPappOrmSession()  # Ensure we have a session maker
        self._ScopedSession.close_all()

    def getPappOrmSession(self):
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

    def migrate(self):
        self.getPappOrmSession()

        isDbInitialised = self._dbEngine.dialect.has_table(
            self._dbEngine.connect(), 'alembic_version',
            schema=self._metadata.schema)

        if isDbInitialised and self._enableCreateAll:
            self._doMigration(self._dbEngine)

        else:
            self._doCreateAll(self._dbEngine)

    def getPgSequenceGenerator(self, Declarative, count, session=None):
        if not count:
            return

        session = session if session else self.getPappOrmSession()
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

        # curdir = os.getcwd()
        # os.chdir(os.path.dirname(peekServerConfig.alembicIniPath))

        # then, load the Alembic configuration and generate the
        # version table, "stamping" it with the most recent rev:
        from alembic.config import Config
        alembic_cfg = Config(configFile.name)
        command(alembic_cfg, *args)

        # os.chdir(curdir)

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