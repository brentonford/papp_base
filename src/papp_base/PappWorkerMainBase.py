class PappWorkerMainBase:

    def __init__(self, platform):
        self._platform = platform
        self._initSelf()

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def unload(self):
        raise NotImplementedError()

    @property
    def celeryAppIncludes(self):
        raise NotImplementedError()

    @property
    def celeryApp(self):
        raise NotImplementedError()

    @property
    def publishedWorkerApi(self, requestingPappName):
        return None

    @property
    def publishedStorageApi(self, requestingPappName):
        return None
