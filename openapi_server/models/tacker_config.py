# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.utils import util


class TackerConfig(Model):
    """
    Own model for the tackerConfig, following the OpenAPI template
    """

    def __init__(
        self, user_id=None, pw=None, auth_url=None, base_url=None
    ):  # noqa: E501
        """TackerConfig
        :param user_id: The user_id of this TackerConfig.  # noqa: E501
        :type user_id: str
        :param pw: The pw of this TackerConfig.  # noqa: E501
        :type pw: str
        :param auth_url: The auth_url of this TackerConfig.  # noqa: E501
        :type auth_url: str
        :param base_url: The base_url of this TackerConfig.  # noqa: E501
        :type base_url: str
        """

        self.openapi_types = {
            "user_id": str,
            "base_url": str,
            "auth_url": str,
            "pw": str,
        }

        # map from config file to internal attr
        self.attribute_map = {
            "user_id": "USER_ID",
            "base_url": "BASEURL",
            "auth_url": "AUTH_URL",
            "pw": "PASSWORD",
        }

        self._user_id = user_id
        self._pw = pw
        self._auth_url = auth_url
        self._base_url = base_url

    @classmethod
    def from_dict(cls, dikt) -> "TackerConfig":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The tackerConfig of this TackerConfig.  # noqa: E501
        :rtype: TackerConfig
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self):
        """Gets the user_id of this TackerConfig.


        :return: The user_id of this TackerConfig.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this TackerConfig.


        :param user_id: The user_id of this TackerConfig.
        :type user_id: str
        """

        self._user_id = user_id

    @property
    def pw(self):
        """Gets the pw of this TackerConfig.


        :return: The pw of this TackerConfig.
        :rtype: str
        """
        return self._pw

    @pw.setter
    def pw(self, pw):
        """Sets the pw of this TackerConfig.


        :param pw: The pw of this TackerConfig.
        :type pw: str
        """

        self._pw = pw

    @property
    def auth_url(self):
        """Gets the auth_url of this TackerConfig.


        :return: The auth_url of this TackerConfig.
        :rtype: str
        """
        return self._auth_url

    @auth_url.setter
    def auth_url(self, auth_url):
        """Sets the auth_url of this TackerConfig.


        :param auth_url: The auth_url of this TackerConfig.
        :type auth_url: str
        """

        self._auth_url = auth_url

    @property
    def base_url(self):
        """Gets the base_url of this TackerConfig.


        :return: The base_url of this TackerConfig.
        :rtype: str
        """
        return self._base_url

    @base_url.setter
    def base_url(self, base_url):
        """Sets the base_url of this TackerConfig.


        :param base_url: The base_url of this TackerConfig.
        :type base_url: str
        """

        self._base_url = base_url
