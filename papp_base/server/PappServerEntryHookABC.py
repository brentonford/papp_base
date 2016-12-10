import os
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.orm.session import Session

from jsoncfg.value_mappers import require_string
from papp_base.PappCommonEntryHookABC import PappCommonEntryHookABC
from papp_base.server.PeekServerPlatformHookABC import PeekServerPlatformHookABC
from papp_base.storage.DbConnBase import DbConnBase


class PappServerEntryHookABC(PappCommonEntryHookABC):
    def __init__(self, pappName: str, pappRootDir: str, platform: PeekServerPlatformHookABC):
        PappCommonEntryHookABC.__init__(self, pappName=pappName, pappRootDir=pappRootDir)
        self._platform = platform

    def migrateStorageSchema(self, metadata: MetaData) -> None:
        """ Initialise the DB

        :param metadata: the SQLAlchemy metadata for this papps schema

        """

        relDir = self._packageCfg.config.storage.alembicDir(require_string)
        alembicDir = os.path.join(self.rootDir, relDir)
        if not os.path.isdir(alembicDir): raise NotADirectoryError(alembicDir)

        self._dbConn = DbConnBase(
            dbConnectString=self.platform.dbConnectString,
            metadata=metadata,
            alembicDir=alembicDir
        )

        self._dbConn.migrate()

    @property
    def dbSession(self) -> Session:
        """ Database Session

        :return: An instance of the sqlalchemy ORM session

        """
        return self._dbConn.getPappOrmSession()

    @property
    def publishedServerApi(self, requestingPappName: str) -> Optional[object]:
        """ Published Server API

        :param requestingPappName: The name of the peek app requesting the API

        :return  class that implements the API that can be used by other PAPPs on this
        platform.
        """
        return None

    @property
    def publishedStorageApi(self, requestingPappName: str) -> Optional[object]:
        """ Published Storage API

        :param requestingPappName: The name of the peek app requesting the API

        :return An object implementing an API that may be used by other apps in
        the platform.
        """
        return None

    @property
    def angularMainModule(self) -> str:
        """ Angular Main Module

        :return: The name of the main module that the Angular2 router will lazy load.
        """
        return self._angularMainModule

    @property
    def angularFrontendDir(self) -> str:
        """ Angular Frontend Dir

        This directory will be linked into the angular app when it is compiled.

        :return: The absolute path of the Angular2 app directory.
        """
        relDir = self._packageCfg.config.papp.title(require_string)
        dir = os.path.join(self._pappRoot, relDir)
        if not os.path.isdir(dir): raise NotADirectoryError(dir)
        return dir
