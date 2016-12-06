import os

from papp_base.storage.DbConnBase import DbConnBase


class PappServerMainBase:
    _title = None
    _angularAdminModule = None

    def __init__(self, platform):
        self._platform = platform
        self._initSelf()

    def _initialiseDb(self, metadata, pappMainFile):
        """ Initialise the DB

        @:param DeclarativeBase the SQLAlchemy declarative base
        @:param pappMainFile the __file__ that inherits this class
        """

        # Configure database
        p = os.path
        pappDir = p.dirname(p.dirname(pappMainFile))

        if p.isdir(p.join(pappDir, "alembic")):
            # Deployed
            alembicDir = p.join(pappDir, "alembic")
        else:
            # Checked out code
            alembicDir = p.join(p.dirname(pappDir), "alembic")

        self._dbConn = DbConnBase(
            dbConnectString=self.platform.dbConnectString,
            metadata=metadata,
            alembicDir=alembicDir
        )

        self._dbConn.migrate()

    def start(self):
        pass

    def stop(self):
        pass

    def unload(self):
        pass

    @property
    def celeryApp(self):
        raise NotImplementedError()

    @property
    def publishedServerApi(self, requestingPappName):
        return None

    @property
    def publishedStorageApi(self, requestingPappName):
        return None

    @property
    def title(self):
        assert self._title is not None
        return self._title

    @property
    def angularAdminModule(self):
        assert self._angularAdminModule is not None
        return self._angularAdminModule
