# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.utils import util


class ContractVNF(Model):
    def __init__(
        self,
        deployment_id=None,
        vnfd_id=None,
        vnf_id=None,
        owner=None,
        parameters=None,
        is_deployed=None,
        is_deleted=None,
    ):  # noqa: E501
        """Vnf - a model defined in OpenAPI

        :param id: The id of this Vnf.  # noqa: E501
        :type id: str
        """
        self.openapi_types = {
            "deployment_id": int,
            "vnfd_id": str,
            "vnf_id": str,
            "owner": str,
            "parameters": str,
            "is_deployed": bool,
            "is_deleted": bool,
        }

        self.attribute_map = {
            "deployment_id": 0,
            "vnfd_id": 1,
            "vnf_id": 2,
            "owner": 3,
            "parameters": 4,
            "is_deployed": 5,
            "is_deleted": 6,
        }

        self._deployment_id = deployment_id
        self._vnfd_id = vnfd_id
        self._vnf_id = vnf_id
        self._owner = owner
        self._parameters = parameters
        self._is_deployed = is_deployed
        self._is_deleted = is_deleted

    @classmethod
    def from_dict(cls, dikt) -> "Vnf":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The vnf of this Vnf.  # noqa: E501
        :rtype: Vnf
        """
        return util.deserialize_model({i: e for i, e in enumerate(dikt)}, cls)

    @property
    def deployment_id(self):
        """Gets the deployment_id of this Vnf.


        :return: The deployment_id of this Vnf.
        :rtype: int
        """
        return self._deployment_id

    @deployment_id.setter
    def deployment_id(self, deployment_id):
        """Sets the deployment_id of this Vnf.


        :param deployment_id: The deployment_id of this Vnf.
        :type deployment_id: int
        """

        self._deployment_id = deployment_id

    @property
    def vnfd_id(self):
        """Gets the vnfd_id of this Vnf.


        :return: The vnfd_id of this Vnf.
        :rtype: str
        """
        return self._vnfd_id

    @vnfd_id.setter
    def vnfd_id(self, vnfd_id):
        """Sets the vnfd_id of this Vnf.


        :param vnfd_id: The vnfd_id of this Vnf.
        :type vnfd_id: str
        """

        self._vnfd_id = vnfd_id

    @property
    def vnf_id(self):
        """Gets the vnf_id of this Vnf.


        :return: The vnf_id of this Vnf.
        :rtype: str
        """
        return self._vnf_id

    @vnf_id.setter
    def vnf_id(self, vnf_id):
        """Sets the vnf_id of this Vnf.


        :param vnf_id: The vnf_id of this Vnf.
        :type vnf_id: str
        """

        self._vnf_id = vnf_id

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
    def is_deployed(self):
        """Gets the is_deployed of this Vnf.


        :return: The is_deployed of this Vnf.
        :rtype: str
        """
        return self._is_deployed

    @is_deployed.setter
    def is_deployed(self, is_deployed):
        """Sets the is_deployed of this Vnf.


        :param is_deployed: The is_deployed of this Vnf.
        :type is_deployed: str
        """

        self._is_deployed = is_deployed

    @property
    def is_deleted(self):
        """Gets the is_deleted of this Vnf.


        :return: The is_deleted of this Vnf.
        :rtype: bool
        """
        return self._is_deleted

    @is_deleted.setter
    def is_deleted(self, is_deleted):
        """Sets the is_deleted of this Vnf.


        :param is_deleted: The is_deleted of this Vnf.
        :type is_deleted: bool
        """

        self._is_deleted = is_deleted
