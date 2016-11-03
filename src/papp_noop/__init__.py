from client.PappClient import PappClient


def makeClient(platformClient):
    return PappClient(platformClient)
