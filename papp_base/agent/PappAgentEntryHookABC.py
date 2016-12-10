from abc import abstractmethod, ABCMeta
from typing import Optional

from papp_base.agent.PeekAgentPlatformABC import PeekAgentPlatformABC


class PappAgentEntryHookABC(metaclass=ABCMeta):

    def __init__(self, platform:PeekAgentPlatformABC):
        self._platform = platform
        self._initSelf()

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
    def publishedAgentApi(self, requestingPappName:str) -> Optional[object]:
        return None
