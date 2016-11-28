class ServerPlatformApiBase:
    @property
    def dbConnectString(self) -> str:
        raise NotImplementedError("dbConnectString")
