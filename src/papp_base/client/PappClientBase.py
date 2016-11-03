class PappClientBase:

    def __init__(self, platformClient):
        self._platformClient = platformClient

    def start(self):
        pass

    def stop(self):
        pass

    def configUrl(self):
        return None
