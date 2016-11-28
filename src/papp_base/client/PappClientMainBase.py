class PappClientMainBase:
    _title = None

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
    def publishedClientApi(self, requestingPappName):
        return None

    @property
    def title(self):
        assert self._title is not None
        return self._title
