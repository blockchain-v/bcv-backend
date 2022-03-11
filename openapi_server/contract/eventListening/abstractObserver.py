from abc import ABCMeta, abstractmethod


class AbstractObserver(metaclass=ABCMeta):
    """
    Abstract observer meta class. This class should be used an interface/ template for the observers.
    Inspired by Sean Bradley's
    `Design Patterns in Python: Common GOF (Gang of Four) Design Patterns implemented in Python` book.
    Using Gang of Four (GoF) naming.
    """

    @staticmethod
    @abstractmethod
    def update(observable, *args, **kwargs):
        """observer should do something here"""
