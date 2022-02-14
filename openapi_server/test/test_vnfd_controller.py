# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.new_vnfd import NewVnfd  # noqa: E501
from openapi_server.models.vnfd import Vnfd  # noqa: E501
from openapi_server.test import BaseTestCase


class TestVnfdController(BaseTestCase):
    """VnfdController integration test stubs"""

    def test_create_vnfd_returns_unauthorized_without_token(self):
        """Test case for create_vnfd

        Creates a new vnf descriptor
        """
        new_vnfd = NewVnfd()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "ApiKeyAuth": "special-key",
        }
        response = self.client.open(
            "/api/v1/bcv/vnfd",
            method="POST",
            headers=headers,
            data=json.dumps(new_vnfd),
            content_type="application/json",
        )
        resp = response.status_code
        self.assertTrue(resp == 401)

    def test_delete_vnfd_returns_unauthorized_without_token(self):
        """Test case for delete_vnfd

        Deletes a vnf descriptor with vnfdID
        """
        headers = {
            "ApiKeyAuth": "special-key",
        }
        response = self.client.open(
            "/api/v1/bcv/vnfd/<vnfdID>", method="DELETE", headers=headers
        )
        resp = response.status_code
        self.assertTrue(resp == 401)

    def test_get_vnfd_returns_unauthorized_without_token(self):
        """Test case for get_vnfd

        Returns a vnf descriptor with vnfdID
        """
        headers = {
            "Accept": "application/json",
            "ApiKeyAuth": "special-key",
        }
        response = self.client.open(
            "/api/v1/bcv/vnfd/<vnfdID>", method="GET", headers=headers
        )
        resp = response.status_code
        self.assertTrue(resp == 401)

    def test_get_vnfds_returns_unauthorized_without_token(self):
        """Test case for get_vnfds

        Returns all vnf descriptors
        """
        headers = {
            "Accept": "application/json",
            "ApiKeyAuth": "special-key",
        }
        response = self.client.open("/api/v1/bcv/vnfd", method="GET", headers=headers)
        resp = response.status_code
        self.assertTrue(resp == 401)


if __name__ == "__main__":
    unittest.main()
