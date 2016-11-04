"""
 * SynNOVA.rdbms.__init__.py
 *
 *  Copyright Synerty Pty Ltd 2013
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by
 *  Synerty Pty Ltd
 *
"""
import logging
from mutex import mutex
from tempfile import NamedTemporaryFile
from time import sleep

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import Sequence

logger = logging.getLogger(__name__)


class SqlaConn(object):
    dbEngine = None
    ScopedSession = None
    dbEngineArgs = {}

    metadata = None
    dbConnectString = None
    alembicDir = None


def setup(dbConnectString, metadata, alembicDir):
    SqlaConn.dbConnectString = dbConnectString
    SqlaConn.metadata = metadata
    SqlaConn.alembicDir = alembicDir


def closeAllSessions():
    getPappOrmSession()  # Ensure we have a session maker
    SqlaConn.ScopedSession.close_all()


def getPappOrmSession():
    assert SqlaConn.dbConnectString

    if SqlaConn.ScopedSession:
        return SqlaConn.ScopedSession()

    SqlaConn.dbEngine = create_engine(
        SqlaConn.dbConnectString,
        echo=False,
        **SqlaConn.dbEngineArgs
    )

    isDbInitialised = SqlaConn.dbEngine.dialect.has_table(
        SqlaConn.dbEngine.connect(), 'alembic_version',
        schema=SqlaConn.metadata.schema)

    if isDbInitialised:
        doMigration(SqlaConn.dbEngine)

    else:
        doCreateAll(SqlaConn.dbEngine)

    SqlaConn.ScopedSession = scoped_session(
        sessionmaker(bind=SqlaConn.dbEngine))

    return SqlaConn.ScopedSession()


sequenceMutex = mutex()


def getPgSequenceGenerator(Declarative, count, session=None):
    if not count:
        return

    session = session if session else getPappOrmSession()
    session.commit()

    while not sequenceMutex.testandset():
        sleep(0.001)

    # Something about the backend not updating curval/nextval causes issues when
    #
    sequence = Sequence('%s_id_seq' % Declarative.__tablename__)
    startId = session.execute(sequence) + 1
    endId = startId + count

    session.execute('alter sequence "%s" restart with %s'
                    % (sequence.name, endId + 1))
    session.commit()

    sequenceMutex.unlock()

    while startId < endId:
        yield startId
        startId += 1


def _runAlembicCommand(command, *args):
    configFile = writeAlembicIni()

    # curdir = os.getcwd()
    # os.chdir(os.path.dirname(peekServerConfig.alembicIniPath))

    # then, load the Alembic configuration and generate the
    # version table, "stamping" it with the most recent rev:
    from alembic.config import Config
    alembic_cfg = Config(configFile.name)
    command(alembic_cfg, *args)

    # os.chdir(curdir)


def doCreateAll(engine):
    SqlaConn.metadata.create_all(SqlaConn.dbEngine)

    from alembic import command
    _runAlembicCommand(command.stamp, "head")


def writeAlembicIni():
    cfg = '''
[alembic]
script_location = %(alembicDir)s
sourceless = true
sqlalchemy.url = %(url)s

[logging]
default_level = INFO
    '''

    p = os.path
    cfg %= {'alembicDir': SqlaConn.alembicDir,
            'url': SqlaConn.dbConnectString}

    tempFile = NamedTemporaryFile()
    tempFile.write(cfg)
    tempFile.flush()
    return tempFile


def doMigration(engine):
    from alembic import command
    _runAlembicCommand(command.upgrade, "head")
