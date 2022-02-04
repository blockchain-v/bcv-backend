# coding: utf-8

from __future__ import absolute_import
import unittest
from mongoengine import connect, disconnect

from flask import json
from six import BytesIO

from openapi_server.models.address_request import AddressRequest  # noqa: E501
from openapi_server.models.token_request import TokenRequest  # noqa: E501
from openapi_server.models.token_response import TokenResponse  # noqa: E501
from openapi_server.test import BaseTestCase
from openapi_server.repositories import User, Nonce


class TestTokenController(BaseTestCase):
    """TokenController integration test stubs"""

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create_nonce(self):
        """Test case for create_nonce

        Creates and returns a new nonce
        """
        address_request = AddressRequest('0xasdf')
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
        mockAddress = '0x474F1243F1Eec4eDfD576425f581Ec1cE3d0A099'
        mockNonce = '0xd0a03f943640495b82d4f4ef64542ff6'
        usr = User(address=mockAddress)
        usr.save()
        nonce = Nonce(address=mockAddress, value=mockNonce)
        nonce.save()
        token_request = TokenRequest(
            signed_nonce='0x250310d02df70e54d9735c76951730db273c790958761c05c31eada50af5d286616d9f70ff6e71c450116e780755ca49a71516c1c6217a42666d2ce9ed3c04481b',
            nonce=mockNonce, address=mockAddress)
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
        self.assert_(response.json.get('isRegistered') == True)


if __name__ == '__main__':
    unittest.main()
