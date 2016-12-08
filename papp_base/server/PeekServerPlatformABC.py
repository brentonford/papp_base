from abc import abstractproperty

from papp_base.PeekPlatformCommonABC import PeekPlatformCommonABC
from papp_base.PeekPlatformFrontendABC import PeekPlatformFrontendABC


class PeekServerPlatformABC(PeekPlatformCommonABC, PeekPlatformFrontendABC):
    @abstractproperty
    def dbConnectString(self) -> str:
        """ DB Connect String

        :return: The SQLAlchemy database engine connection string/url.

        """
