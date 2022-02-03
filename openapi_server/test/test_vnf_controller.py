# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.vnf import Vnf  # noqa: E501
from openapi_server.test import BaseTestCase


class TestVnfController(BaseTestCase):
    """VnfController integration test stubs"""

    def test_get_vnf(self):
        """Test case for get_vnf

        Returns vnf details for a specific vnfID
        """
        headers = { 
            'Accept': 'application/json',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/bcv/vnf/<vnfID>',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_vnfs(self):
        """Test case for get_vnfs

        Returns all vnf details for a user
        """
        headers = { 
            'Accept': 'application/json',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/bcv/vnf',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
