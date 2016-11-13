class PeekWorkerApiBase:
    @property
    def celeryApp(self):
        raise NotImplementedError()

    def configureCeleryApp(self, pappCeleryApp):
        raise NotImplementedError()

    @property
    def dbEngine(self):
        raise NotImplementedError()

    @property
    def dbSession(self):
        raise NotImplementedError()
