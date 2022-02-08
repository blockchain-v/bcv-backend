from abc import ABCMeta, abstractmethod


class AbstractObserver(metaclass=ABCMeta):
    """
    Abstract observer meta class. This class should be used an interface/ template for the observers.
    """

    @staticmethod
    @abstractmethod
    def update(observable, *args, **kwargs):
        """ observer should do something here """
