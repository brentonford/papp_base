from abc import abstractproperty

from papp_base.PeekPlatformCommonHookABC import PeekPlatformCommonHookABC
from papp_base.PeekPlatformFrontendHookABC import PeekPlatformFrontendHookABC


class PeekServerPlatformHookABC(PeekPlatformCommonHookABC, PeekPlatformFrontendHookABC):
    @abstractproperty
    def dbConnectString(self) -> str:
        """ DB Connect String

        :return: The SQLAlchemy database engine connection string/url.

        """
