from __future__ import absolute_import
import unittest
from mongoengine import connect, disconnect, DoesNotExist
from openapi_server.repositories import User, Nonce
from openapi_server.services.tokenService import TokenService
from openapi_server.models import AddressRequest, TokenRequest


mock_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZGRyZXNzIjoiMHg0NzRGMTI0M0YxRWVjNGVEZkQ1NzY0MjVmNTgxRWMxY0UzZDBBMDk5IiwiZXhwIjoxNjQ0ODcyNzMxfQ.Qj9G4z1bfydmMXOwvNGLG6WD3JzLfGmeGaoE4phUct4"
mock_addr = "0x474F1243F1Eec4eDfD576425f581Ec1cE3d0A099"
mock_nonce = "0xb95800117462477598a3d8a30beae350"
mock_signed_nonce = "0xa5faa1a935e0a0034d450507e586a0e60519d857f05a5b53fdaf7e3515ff9b3c4d86013664e6f72fe08f3ff99328f7643608e757b239f3ee1267c4e757fda9041c"
mock_signed_address = "0x42edf35e2b88595c0cc96b34a755fef74d0fcd547e14e707adfa63c6704843262fc369d45351601c76a9aa510a69c9227387cd7ac0bb523408d2c48f57753a901c"


class TestTokenService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect("mongoenginetest", host="mongomock://localhost")

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def tearDown(self):
        Nonce.objects().delete()
        User.objects().delete()

    def test_create_nonce_returns_403_for_invalid_address(self):
        adr_req = AddressRequest.from_dict({"address": "asdf"})
        try:
            res = TokenService.create_nonce(adr_req)
        except Exception as e:
            self.assertTrue(e.code == 403)

    def test_create_nonce_returns_201(self):
        adr_req = AddressRequest.from_dict({"address": mock_addr})
        res, code = TokenService.create_nonce(adr_req)
        self.assertTrue(code == 201)
        self.assertTrue(res["nonce"] is not None)

    def test_create_nonce_handler_deletes_old_nonces_for_same_user(self):
        Nonce(value="asdf", address=mock_addr).save()
        res = TokenService.create_nonce_handler(mock_addr)
        try:
            n = Nonce.objects.get(value="asdf")
        except DoesNotExist:
            self.assertTrue(res is not None)

    def test_create_token_handler_returns_false_if_not_in_db(self):
        self.assertFalse(
            TokenService.create_token_handler(
                nonce=mock_nonce,
                signed_nonce=mock_signed_nonce,
                address=mock_addr,
                secret="12345678",
            )
        )

    def test_create_token_handler_returns_(self):
        Nonce(value=mock_nonce, address=mock_addr).save()
        tok = TokenService.create_token_handler(
            nonce=mock_nonce,
            signed_nonce=mock_signed_nonce,
            address=mock_addr,
            secret="12345678",
        )
        self.assertTrue(tok is not None)

    def test_create_token_returns_200_if_user_not_registered(self):
        tk_req = TokenRequest.from_dict(
            {
                "signed_nonce": mock_signed_nonce,
                "nonce": mock_nonce,
                "address": mock_addr,
            }
        )
        res, code = TokenService.create_token(tk_req)
        self.assertTrue(code == 200)

    def test_create_token_returns_403_upon_error(self):
        User(address=mock_addr).save()
        tk_req = TokenRequest.from_dict(
            {
                "signed_nonce": mock_signed_nonce,
                "nonce": mock_nonce,
                "address": mock_addr,
            }
        )
        res, code = TokenService.create_token(tk_req)
        self.assertTrue(code == 403)

    def test_create_token_returns_401(self):
        User(address=mock_addr).save()
        Nonce(value=mock_nonce, address=mock_addr).save()
        tk_req = TokenRequest.from_dict(
            {
                "signedNonce": mock_signed_nonce,
                "nonce": mock_nonce,
                "address": mock_addr,
            }
        )
        res, code = TokenService.create_token(tk_req)
        try:
            n = Nonce.objects.get(value=mock_nonce)
        except DoesNotExist:
            self.assertTrue(code == 201)
            self.assertTrue(res["isRegistered"])
            self.assertTrue(res["token"] is not None)


if __name__ == "__main__":
    unittest.main()
