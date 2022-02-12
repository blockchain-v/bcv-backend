# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.utils import util


class TackerErrorModel(Model):
    def __init__(self, type=None, message=None, detail=None):  # noqa: E501
        """TackerError - a model defined in OpenAPI

        :param message: The message of this TackerError.  # noqa: E501
        :type message: str
        """
        self.openapi_types = {
            "message": str,
            "type": str,
            "detail": str,
        }

        self.attribute_map = {
            "message": "message",
            "type": "type",
            "detail": "detail",
        }

        self._message = message
        self._type = type
        self._detail = detail

    @classmethod
    def from_dict(cls, dikt) -> "TackerError":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The tackerError of this TackerError.  # noqa: E501
        :rtype: TackerError
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self):
        """Gets the message of this TackerErrorModel.


        :return: The message of this TackerErrorModel.
        :rtype: int
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this TackerErrorModel.


        :param message: The message of this TackerErrorModel.
        :type message: str
        """

        self._message = message

    @property
    def type(self):
        """Gets the type of this TackerErrorModel.


        :return: The type of this TackerErrorModel.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this TackerErrorModel.


        :param type: The type of this TackerErrorModel.
        :type type: str
        """

        self._type = type

    @property
    def detail(self):
        """Gets the detail of this TackerErrorModel.


        :return: The detail of this TackerErrorModel.
        :rtype: str
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """Sets the detail of this TackerErrorModel.


        :param detail: The detail of this TackerErrorModel.
        :type detail: str
        """

        self._detail = detail
