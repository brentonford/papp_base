from abc import ABCMeta


class PappServerEntryHookABC(metaclass=ABCMeta):
    def __init__(self, pappRootDir: str, platform: PeekServerPlatformABC):
        self._platform = platform
        self._pappRootDir = pappRootDir
        self._packageCfg = PappPackageFileConfig(pappRootDir)