from twisted.internet import reactor


class PappClient():
    def __init__(self, platformClient):
        print "PappClient initialised"
        self._startLaterCall = None

    def start(self):
        def started():
            self._startLaterCall = None
            print "PappClient started"

        self._startLaterCall = reactor.callLater(3.0, started)

    def stop(self):
        if self._startLaterCall:
            self._startLaterCall.cancel()
        print "PappClient stop"

    def configUrl(self):
        return 'peek_noop'
