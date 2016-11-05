class PappServerMainBase:

    def __init__(self, platform):
        self._platform = platform
        self._initSelf()

    def start(self):
        pass

    def stop(self):
        pass

    def unload(self):
        pass

    def configUrl(self):
        return None

    @property
    def publishedClientApi(self, requestingPappName):
        return None

    @property
    def publishedServerApi(self, requestingPappName):
        return None

    @property
    def publishedStorageApi(self, requestingPappName):
        return None

