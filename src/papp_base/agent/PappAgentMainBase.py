class PappAgentMainBase:

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
    def publishedAgentApi(self, requestingPappName):
        return None
