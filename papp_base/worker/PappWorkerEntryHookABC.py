from abc import abstractproperty

from celery.app.base import Celery

from papp_base.PappCommonEntryHookABC import PappCommonEntryHookABC
from papp_base.worker.PeekWorkerPlatformHookABC import PeekWorkerPlatformHookABC


class PappWorkerEntryHookABC(PappCommonEntryHookABC):
    def __init__(self, pappName: str, pappRootDir: str, platform: PeekWorkerPlatformHookABC):
        PappCommonEntryHookABC.__init__(self, pappName=pappName, pappRootDir=pappRootDir)
        self._platform = platform


    @abstractproperty
    def celeryAppIncludes(self) -> [str]:
        """ Celery App Includes

        This property returns the absolout package paths to the modules with the tasks
        :Example: ["papp_noop.worker.NoopWorkerTask"]

        :return: A list of package+module names that Celery should import.

        """

    @abstractproperty
    def celeryApp(self)-> Celery:
        """ Celery App

        Return the workers instance of the celery app.

        This will be configured with the platforms celery setup.

        """

    # There are no APIs
    # The worker threads can't access this.
