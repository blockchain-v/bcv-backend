# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.utils import util


class Vnf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None):  # noqa: E501
        """Vnf - a model defined in OpenAPI

        :param id: The id of this Vnf.  # noqa: E501
        :type id: str
        """
        self.openapi_types = {
            'id': str
        }

        self.attribute_map = {
            'id': 'id'
        }

        self._id = id

    @classmethod
    def from_dict(cls, dikt) -> 'Vnf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The vnf of this Vnf.  # noqa: E501
        :rtype: Vnf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Vnf.


        :return: The id of this Vnf.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Vnf.


        :param id: The id of this Vnf.
        :type id: str
        """

        self._id = id