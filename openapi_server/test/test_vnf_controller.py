# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.vnf import Vnf  # noqa: E501
from openapi_server.test import BaseTestCase


class TestVnfController(BaseTestCase):
    """VnfController integration test stubs"""

    def test_get_vnf_returns_unauthorized_without_token(self):
        """Test case for get_vnf

        Returns vnf details for a specific vnfID
        """
        headers = {
            "Accept": "application/json",
            "ApiKeyAuth": "special-key",
        }
        response = self.client.open(
            "/api/v1/bcv/vnf/<vnfID>", method="GET", headers=headers
        )
        resp = response.status_code
        self.assertTrue(resp == 401)

    def test_get_vnfs_returns_unauthorized_without_token(self):
        """Test case for get_vnfs

        Returns all vnf details for a user
        """
        headers = {
            "Accept": "application/json",
            "ApiKeyAuth": "special-key",
        }
        response = self.client.open("/api/v1/bcv/vnf", method="GET", headers=headers)
        resp = response.status_code
        self.assertTrue(resp == 401)


if __name__ == "__main__":
    unittest.main()
