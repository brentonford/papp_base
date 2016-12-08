import os
from abc import ABCMeta, abstractmethod
from typing import Optional

from papp_base.client.PeekClientPlatformABC import PeekClientPlatformABC


class PappClientEntryHookABC(metaclass=ABCMeta):

    def __init__(self, platform: PeekClientPlatformABC):
        self._platform = platform
        self.load()

    def _setupDirs(self, pappMainFile: str):
        p = os.path
        pappDir = p.dirname(p.dirname(pappMainFile))

        frontendDir = p.join(pappDir, self._angularFrontendDir)
        if not p.isdir(frontendDir):
            raise Exception("%s doesn't exist", frontendDir)
        self._angularAdminModule = frontendDir

    @abstractmethod
    def load(self):
        pass


    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def unload(self):
        pass

    @property
    def publishedClientApi(self, requestingPappName: str) -> Optional[object]:
        return None

    @property
    def title(self) -> str:
        assert self._title is not None
        return self._title

    @property
    def angularAdminModule(self) -> str:
        assert self._angularAdminModule is not None
        return self._angularAdminModule

    @property
    def frontendDir(self) -> str:
        assert self._angularFrontendDir is not None
        return self._angularFrontendDir
