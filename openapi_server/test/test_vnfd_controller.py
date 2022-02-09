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

    def test_create_vnfd(self):
        """Test case for create_vnfd

        Creates a new vnf descriptor
        """
        new_vnfd = openapi_server.NewVnfd()
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
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_delete_vnfd(self):
        """Test case for delete_vnfd

        Deletes a vnf descriptor with vnfdID
        """
        headers = {
            "ApiKeyAuth": "special-key",
        }
        response = self.client.open(
            "/api/v1/bcv/vnfd/<vnfdID>", method="DELETE", headers=headers
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_vnfd(self):
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
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_vnfds(self):
        """Test case for get_vnfds

        Returns all vnf descriptors
        """
        headers = {
            "Accept": "application/json",
            "ApiKeyAuth": "special-key",
        }
        response = self.client.open("/api/v1/bcv/vnfd", method="GET", headers=headers)
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
