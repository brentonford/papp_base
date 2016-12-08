from abc import ABCMeta, abstractmethod, abstractproperty

from papp_base.worker.PeekWorkerProviderABC import PeekWorkerProviderABC


class PappWorkerEntryHookABC(metaclass=ABCMeta):

    def __init__(self, pappRootDir:str, platform:PeekWorkerProviderABC):
        self._platform = platform
        self._pappRootDir = pappRootDir

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

    @abstractproperty
    def celeryAppIncludes(self):
        pass

    @abstractproperty
    def celeryApp(self):
        pass

    # There are no APIs
    # The worker threads can't access this.
