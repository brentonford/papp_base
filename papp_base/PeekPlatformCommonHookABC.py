from abc import ABCMeta, abstractmethod
from typing import Optional


class PeekPlatformCommonHookABC(metaclass=ABCMeta):

    @abstractmethod
    def getOtherPappApi(self, pappName:str) -> Optional[object]:
        """ Get Other Papp Api

        Asks the papp for it's api object and return it to this papp.
        The API returned matches the platform service.

        :param pappName: The name of the papp to retrieve the API for
        :return: An instance of the other papps API for this Peek Platform Service.

        """
