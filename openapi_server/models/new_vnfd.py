# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.utils import util


class NewVnfd(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, attributes=None, name=None, description=None):  # noqa: E501
        """NewVnfd - a model defined in OpenAPI

        :param attributes: The attributes of this NewVnfd.  # noqa: E501
        :type attributes: object
        :param name: The name of this NewVnfd.  # noqa: E501
        :type name: str
        :param description: The description of this NewVnfd.  # noqa: E501
        :type description: str
        """
        self.openapi_types = {"attributes": object, "name": str, "description": str}

        self.attribute_map = {
            "attributes": "attributes",
            "name": "name",
            "description": "description",
        }

        self._attributes = attributes
        self._name = name
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> "NewVnfd":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The newVnfd of this NewVnfd.  # noqa: E501
        :rtype: NewVnfd
        """
        return util.deserialize_model(dikt, cls)

    @property
    def attributes(self):
        """Gets the attributes of this NewVnfd.


        :return: The attributes of this NewVnfd.
        :rtype: object
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this NewVnfd.


        :param attributes: The attributes of this NewVnfd.
        :type attributes: object
        """

        self._attributes = attributes

    @property
    def name(self):
        """Gets the name of this NewVnfd.


        :return: The name of this NewVnfd.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NewVnfd.


        :param name: The name of this NewVnfd.
        :type name: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this NewVnfd.


        :return: The description of this NewVnfd.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this NewVnfd.


        :param description: The description of this NewVnfd.
        :type description: str
        """

        self._description = description
