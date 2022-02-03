# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.address_request import AddressRequest  # noqa: E501
from openapi_server.models.nonce import Nonce  # noqa: E501
from openapi_server.models.token_request import TokenRequest  # noqa: E501
from openapi_server.models.token_response import TokenResponse  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTokenController(BaseTestCase):
    """TokenController integration test stubs"""

    def test_create_nonce(self):
        """Test case for create_nonce

        Creates and returns a new nonce
        """
        address_request = openapi_server.AddressRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/bcv/token',
            method='PUT',
            headers=headers,
            data=json.dumps(address_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_token(self):
        """Test case for create_token

        Creates and returns a new token. Requires a nonce.
        """
        token_request = openapi_server.TokenRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/bcv/token',
            method='POST',
            headers=headers,
            data=json.dumps(token_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
