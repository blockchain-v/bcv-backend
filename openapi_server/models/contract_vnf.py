# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.utils import util


class ContractVNF(Model):

    def __init__(self, deploymentId=None, vnfdId=None, vnfId=None, owner=None, parameters=None, isDeployed=None,
                 isDeleted=None):  # noqa: E501
        """Vnf - a model defined in OpenAPI

        :param id: The id of this Vnf.  # noqa: E501
        :type id: str
        """
        self.openapi_types = {
            'deploymentId': int,
            'vnfdId': str,
            'vnfId': str,
            'owner': str,
            'parameters': str,
            'isDeployed': bool,
            'isDeleted': bool
        }

        self.attribute_map = {
            'deploymentId': 0,
            'vnfdId': 1,
            'vnfId': 2,
            'owner': 3,
            'parameters': 4,
            'isDeployed': 5,
            'isDeleted': 6
        }

        self._deploymentId = deploymentId
        self._vnfdId = vnfdId
        self._vnfId = vnfId
        self._owner = owner
        self._parameters = parameters
        self._isDeployed = isDeployed
        self._isDeleted = isDeleted

    @classmethod
    def from_dict(cls, dikt) -> 'Vnf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The vnf of this Vnf.  # noqa: E501
        :rtype: Vnf
        """
        return util.deserialize_model({i:e for i,e in enumerate(dikt)}, cls)

    @property
    def deploymentId(self):
        """Gets the deploymentId of this Vnf.


        :return: The deploymentId of this Vnf.
        :rtype: int
        """
        return self._deploymentId

    @deploymentId.setter
    def deploymentId(self, deploymentId):
        """Sets the deploymentId of this Vnf.


        :param deploymentId: The deploymentId of this Vnf.
        :type deploymentId: int
        """

        self._deploymentId = deploymentId

    @property
    def vnfdId(self):
        """Gets the vnfdId of this Vnf.


        :return: The vnfdId of this Vnf.
        :rtype: str
        """
        return self._vnfdId

    @vnfdId.setter
    def vnfdId(self, vnfdId):
        """Sets the vnfdId of this Vnf.


        :param vnfdId: The vnfdId of this Vnf.
        :type vnfdId: str
        """

        self._vnfdId = vnfdId

    @property
    def vnfId(self):
        """Gets the vnfId of this Vnf.


        :return: The vnfId of this Vnf.
        :rtype: str
        """
        return self._vnfId

    @vnfId.setter
    def vnfId(self, vnfId):
        """Sets the vnfId of this Vnf.


        :param vnfId: The vnfId of this Vnf.
        :type vnfId: str
        """

        self._vnfId = vnfId

    @property
    def owner(self):
        """Gets the owner of this Vnf.


        :return: The owner of this Vnf.
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this Vnf.


        :param owner: The owner of this Vnf.
        :type owner: str
        """

        self._owner = owner

    @property
    def parameters(self):
        """Gets the parameters of this Vnf.


        :return: The parameters of this Vnf.
        :rtype: str
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this Vnf.


        :param parameters: The parameters of this Vnf.
        :type parameters: str
        """

        self._parameters = parameters

    @property
    def isDeployed(self):
        """Gets the isDeployed of this Vnf.


        :return: The isDeployed of this Vnf.
        :rtype: str
        """
        return self._isDeployed

    @isDeployed.setter
    def isDeployed(self, isDeployed):
        """Sets the isDeployed of this Vnf.


        :param isDeployed: The isDeployed of this Vnf.
        :type isDeployed: str
        """

        self._isDeployed = isDeployed


    @property
    def isDeleted(self):
        """Gets the isDeleted of this Vnf.


        :return: The isDeleted of this Vnf.
        :rtype: bool
        """
        return self._isDeleted

    @isDeleted.setter
    def isDeleted(self, isDeleted):
        """Sets the isDeleted of this Vnf.


        :param isDeleted: The isDeleted of this Vnf.
        :type isDeleted: bool
        """

        self._isDeleted = isDeleted
