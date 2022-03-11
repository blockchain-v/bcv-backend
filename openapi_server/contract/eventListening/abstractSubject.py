from abc import ABCMeta, abstractmethod


class AbstractSubject(metaclass=ABCMeta):
    """
    AbstractSubject meta class.
    This class should be used as an interface / template for the observer pattern
    Inspired by Sean Bradley's
    `Design Patterns in Python: Common GOF (Gang of Four) Design Patterns implemented in Python` book.
    Using Gang of Four (GoF) naming.
    """

    @staticmethod
    @abstractmethod
    def attach(observer):
        """attach observer"""

    @staticmethod
    @abstractmethod
    def detach(observer):
        """detach observer"""

    @staticmethod
    @abstractmethod
    def notifyObservers(observer):
        """notify all observers"""
