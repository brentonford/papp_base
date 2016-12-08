import os
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.orm.session import Session

from jsoncfg.value_mappers import require_string, require_array
from papp_base.PappPackageFileConfig import PappPackageFileConfig
from papp_base.server.PeekServerProviderABC import PeekServerProviderABC
from papp_base.storage.DbConnBase import DbConnBase


class PappServerEntryHookABC(metaclass=ABCMeta):
    def __init__(self, pappRootDir: str, platform: PeekServerProviderABC):
        self._platform = platform
        self._pappRootDir = pappRootDir
        self._packageCfg = PappPackageFileConfig(pappRootDir)

    @property
    def requiresServer(self) -> bool:
        """ Requires Server

        Determines if this papp requires the platforms server service from the
        papp_package.json

        :return: True if this papp requires the server service

        """
        return "server" in self._packageCfg.config.requiresServices(require_array)

    @property
    def requiresStorage(self) -> bool:
        """ Requires Storage

        Determines if this papp requires the platforms storage "service" from the
        papp_package.json

        :return: True if this papp requires use of the storage database

        """
        return "storage" in self._packageCfg.config.requiresServices(require_array)

    def migrateStorageSchema(self, metadata: MetaData) -> None:
        """ Initialise the DB

        :param metadata: the SQLAlchemy metadata for this papps schema

        """

        relDir = self._packageCfg.config.storage.alembicDir(require_string)
        alembicDir = os.path.join(self._pappRoot, relDir)
        if not os.path.isdir(alembicDir): raise NotADirectoryError(alembicDir)

        self._dbConn = DbConnBase(
            dbConnectString=self.platform.dbConnectString,
            metadata=metadata,
            alembicDir=alembicDir
        )

        self._dbConn.migrate()

    @property
    def dbSession(self) -> Session:
        return self._dbConn.getPappOrmSession()

    @abstractmethod
    def load(self)-> None:
        """ Load


        """

    @abstractmethod
    def start(self) -> None:
        """ Start

        This method is called by the platform when the papp should start
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload

        This method is called after stop is called, to unload any last resources
        before the PAPP is unlinked from the platform
        """
        pass

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
    def title(self) -> str:
        """ Peek App Title
        :return the title of this papp
        """
        return self._packageCfg.config.papp.title(require_string)

    @property
    def angularMainModule(self) -> str:
        return self._angularMainModule

    @property
    def angularFrontendDir(self) -> str:
        relDir = self._packageCfg.config.papp.title(require_string)
        dir = os.path.join(self._pappRoot, relDir)
        if not os.path.isdir(dir): raise NotADirectoryError(dir)
        return dir
