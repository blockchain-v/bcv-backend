from __future__ import absolute_import
import unittest
from mongoengine import connect, disconnect, DoesNotExist
from openapi_server.repositories import User, Nonce
from openapi_server.services.userService import UserService
from openapi_server.models import AddressRequest, TokenRequest

mock_addr = "0x474F1243F1Eec4eDfD576425f581Ec1cE3d0A099"
mock_signed_address = "0x42edf35e2b88595c0cc96b34a755fef74d0fcd547e14e707adfa63c6704843262fc369d45351601c76a9aa510a69c9227387cd7ac0bb523408d2c48f57753a901c"


class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect("mongoenginetest", host="mongomock://localhost")

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def tearDown(self):
        Nonce.objects().delete()
        User.objects().delete()

    def test_is_user_registered_returns_false_if_not_registered(self):
        self.assertFalse(UserService.is_user_registered("asdf"))

    def test_is_user_registered_returns_true_if_registered(self):
        User(address="asdf").save()
        self.assertTrue(UserService.is_user_registered("asdf"))

    def test_unregister_deletes_user(self):
        User(address="asdf").save()
        UserService.unregister({"user": "asdf"})
        try:
            n = User.objects.get(address="asdf")
            self.assertFalse(True)
        except DoesNotExist:
            self.assertFalse(False)

    def test_register(self):
        UserService.register({"user": mock_addr, "signedAddress": mock_signed_address})
        u = User.objects.get(address=mock_addr)
        self.assertTrue(u.address == mock_addr)


if __name__ == "__main__":
    unittest.main()
