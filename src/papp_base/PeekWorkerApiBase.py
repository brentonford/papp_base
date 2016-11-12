class PeekWorkerApiBase:
    @property
    def celeryApp(self):
        raise NotImplementedError()

    def configureCeleryApp(self, pappCeleryApp):
        raise NotImplementedError()
