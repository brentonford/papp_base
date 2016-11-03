from client.PappClientBase import PappClient


def makeClient(platformClient):
    return PappClient(platformClient)
