from abc import ABCMeta, abstractproperty, abstractmethod
from typing import Mapping


class PeekWorkerProviderABC(metaclass=ABCMeta):
    # @abstractproperty
    # def celeryApp(self):
    #     """ Celery App
    #
    #     :return The peek worker, main celery app
    #     """
    #     pass

    @abstractmethod
    def configureCeleryApp(self, pappCeleryApp) -> Mapping:
        """ Configure Celery App

        Setup the this papps celery app to work with this environment
        set backend, broker, serialsation, etc

        :param pappCeleryApp: The papp celery app.

        """
        raise NotImplementedError()

    @abstractproperty
    def dbEngine(self):
        """ DB Engine

        :return: An instance of the SQLAclemy db engine for this worker
        """
        raise NotImplementedError()

    @abstractproperty
    def dbSession(self):
        """ DB Session

        :return: An instance of the SQLAlchemt DB Session for this worker
        """
        raise NotImplementedError()
