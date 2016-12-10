import os
from typing import Optional

from jsoncfg.value_mappers import require_string
from papp_base.PappCommonEntryHookABC import PappCommonEntryHookABC
from papp_base.client.PeekClientPlatformHookABC import PeekClientPlatformHookABC


class PappClientEntryHookABC(PappCommonEntryHookABC):
    def __init__(self, pappName: str, pappRootDir: str, platform: PeekClientPlatformHookABC):
        PappCommonEntryHookABC.__init__(self, pappName=pappName, pappRootDir=pappRootDir)
        self._platform = platform

    @property
    def publishedClientApi(self, requestingPappName: str) -> Optional[object]:
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
