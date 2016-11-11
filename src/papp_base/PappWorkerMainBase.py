class PappWorkerMainBase:

    def __init__(self, platform):
        self._platform = platform
        self._initSelf()

    def start(self):
        pass

    def stop(self):
        pass

    def unload(self):
        pass

    @property
    def publishedWorkerApi(self, requestingPappName):
        return None

    @property
    def publishedStorageApi(self, requestingPappName):
        return None
