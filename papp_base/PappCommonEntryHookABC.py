from abc import ABCMeta, abstractmethod

from jsoncfg.value_mappers import require_string
from papp_base.PappPackageFileConfig import PappPackageFileConfig


class PappCommonEntryHookABC(metaclass=ABCMeta):
    def __init__(self, pappName:str, pappRootDir:str):
        self._pappName = pappName
        self._pappRootDir = pappRootDir
        self._packageCfg = PappPackageFileConfig(pappRootDir)

    @property
    def name(self) -> str:
        """ Papp Name

        :return: The name of this papp
        """
        return self._pappName

    @property
    def rootDir(self) -> str:
        """ Papp Root Dir

        :return: The absolute directory where the Papp package is located.
        """
        return self._pappRootDir

    @property
    def packageCfg(self) -> PappPackageFileConfig:
        """ Package Config

        :return: A reference to the papp_package.json loader object (see json-cfg)
        """
        return self._packageCfg

    @abstractmethod
    def load(self) -> None:
        """ Load

        This will be called when the papp is loaded, just after the db is migrated.
        Place any custom initialiastion steps here.

        """

    @abstractmethod
    def start(self) -> None:
        """ Start

        This method is called by the platform when the papp should start
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """ Stop

        This method is called by the platform to tell the peek app to shutdown and stop
        everything it's doing
        """
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload

        This method is called after stop is called, to unload any last resources
        before the PAPP is unlinked from the platform
        """
        pass

    @property
    def title(self) -> str:
        """ Peek App Title
        :return the title of this papp
        """
        return self._packageCfg.config.papp.title(require_string)
