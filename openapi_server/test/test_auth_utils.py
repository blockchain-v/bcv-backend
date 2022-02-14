from __future__ import absolute_import
import unittest
from mongoengine import connect, disconnect
from openapi_server.repositories import User, Nonce
from werkzeug.exceptions import abort, HTTPException
from datetime import datetime, timedelta

from openapi_server.utils.auth_utils import (
    decode_token,
    get_address_from_token,
    verify_token,
    authorize,
    verify_nonce,
    _recover_address,
    _check_auth_for_address,
    _check_auth_for_nonce,
    check_auth,
)

mock_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZGRyZXNzIjoiMHg0NzRGMTI0M0YxRWVjNGVEZkQ1NzY0MjVmNTgxRWMxY0UzZDBBMDk5IiwiZXhwIjoxNjQ0ODcyNzMxfQ.Qj9G4z1bfydmMXOwvNGLG6WD3JzLfGmeGaoE4phUct4"
mock_addr = "0x474F1243F1Eec4eDfD576425f581Ec1cE3d0A099"
mock_nonce = "0xb95800117462477598a3d8a30beae350"
mock_signed_nonce = "0xa5faa1a935e0a0034d450507e586a0e60519d857f05a5b53fdaf7e3515ff9b3c4d86013664e6f72fe08f3ff99328f7643608e757b239f3ee1267c4e757fda9041c"
mock_signed_address = "0x42edf35e2b88595c0cc96b34a755fef74d0fcd547e14e707adfa63c6704843262fc369d45351601c76a9aa510a69c9227387cd7ac0bb523408d2c48f57753a901c"

mock_nonce_2 = "0x8e5f90b77d4146d98cc8c25f24d69b03"
mock_signed_nonce_2 = "0xc1496ef56bb9365cab738d39b1223523dee9012bbafae072bae1e8669a7e562d6ed4281d62c634fdf16cd50f80d685d9ebc53e7027d7f5f574cacfe2f8fc36f91c"
mock_addr_2 = "0x480EEaAfD230a57558b6Dfc79CF075CDf3033F73"


class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect("mongoenginetest", host="mongomock://localhost")

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def tearDown(self):
        Nonce.objects().delete()
        User.objects().delete()

    def test_decode_token(self):
        res = decode_token(mock_token, "12345678")
        self.assertTrue(res["address"] == mock_addr)

    def test_get_address_from_token(self):
        self.assertTrue(get_address_from_token(mock_token) == mock_addr)

    def test_get_address_from_token_returns_false_if_invalid_token(self):
        self.assertFalse(get_address_from_token("asdf"))

    def test_verify_token_returns_false_if_no_user(self):
        self.assertFalse(verify_token(mock_token))

    def test_verify_token_returns_true_if_user(self):
        User(address=mock_addr).save()
        self.assertTrue(verify_token(mock_token))

    def test_authorize_returns_user_address(self):
        User(address=mock_addr).save()
        res = authorize(mock_token)
        self.assertTrue(res["userAddress"] == mock_addr)

    def test_authorize_returns_401(self):
        User(address=mock_addr).save()
        try:
            res = authorize("1234")
            print("res", res)
        except HTTPException as e:
            self.assertTrue(e.code == 401)

    def test_check_auth_for_address(self):
        self.assertTrue(_check_auth_for_address(mock_addr, mock_signed_address))

    def test_check_auth_for_address_returns_false_for_invalid_signed_addr(self):
        # ValueError case
        inv_signed_addr = "0x42edf35e2b88595c0cc96b34a755fef74d0fcd547e14e707adfa63c6704843262fc369d45351601c76a9aa510a69c9227387cd7ac0bb523408d2c48f57753a901f"
        self.assertFalse(_check_auth_for_address(mock_addr, inv_signed_addr))

    def test_check_auth_for_address_returns_false_for_invalid_addr(self):
        # claimed addr != addr
        other_addr = "0x1192Ad74Ee4983a039710558D3b114bA81B1aC03"
        self.assertFalse(_check_auth_for_address(other_addr, mock_signed_address))

    def test_check_auth_for_address_returns_false_for_invalid_addr_format(self):
        # InvalidAddress case
        inv_addr = "0x119C03"
        self.assertFalse(_check_auth_for_address(inv_addr, mock_signed_address))

    def test_check_auth_for_address_returns_false_for_invalid_signed_addr_format(self):
        # ValueError
        inv_signed_addr = "0x119C03"
        self.assertFalse(_check_auth_for_address(mock_addr, inv_signed_addr))

    """
    Nonces
    """

    def test_verify_nonce_returns_false_if_not_exists(self):
        self.assertFalse(verify_nonce("asdf", mock_addr))

    def test_verify_nonce_returns_true_if_time_valid(self):
        Nonce(value="asdf", address=mock_addr).save()
        self.assertTrue(verify_nonce("asdf", mock_addr))

    def test_verify_nonce_returns_false_if_time_invalid(self):
        ystrday = datetime.today() - timedelta(days=1, minutes=1)

        n = Nonce(value="asdf", address=mock_addr, issueDate=ystrday).save()
        print(n.issueDate)
        self.assertFalse(verify_nonce("asdf", mock_addr))

    def test_check_auth_for_nonce_returns_false_if_not_in_db(self):
        self.assertFalse(
            _check_auth_for_nonce(mock_nonce, mock_signed_nonce, mock_addr)
        )

    def test_check_auth_for_nonce_returns_true(self):
        Nonce(value=mock_nonce, address=mock_addr).save()
        self.assertTrue(_check_auth_for_nonce(mock_nonce, mock_signed_nonce, mock_addr))

    def test_check_auth_for_nonce_returns_true_2(self):
        Nonce(value=mock_nonce_2, address=mock_addr_2).save()
        self.assertTrue(
            _check_auth_for_nonce(mock_nonce_2, mock_signed_nonce_2, mock_addr_2)
        )

    def test_check_auth_for_nonce_returns_false_from_invalid_signed_nonce(self):
        # address != user_address
        Nonce(value=mock_nonce, address=mock_addr).save()
        self.assertFalse(
            _check_auth_for_nonce(mock_nonce, mock_signed_nonce_2, mock_addr)
        )

    def test_check_auth_for_nonce_returns_false_from_invalid_signed_nonce_format(self):
        # address != user_address
        sign_nonce = "asdf"
        Nonce(value=mock_nonce, address=mock_addr).save()
        self.assertFalse(_check_auth_for_nonce(mock_nonce, sign_nonce, mock_addr))

    def test_check_auth_returns_false_if_addr_is_missing_for_addr_check(self):
        # InvalidAddress in _check_auth_for_address
        self.assertFalse(
            check_auth(claim=mock_nonce_2, signed_claim=mock_signed_nonce_2)
        )

    def test_check_auth_returns_false(self):
        # InvalidAddress in _check_auth_for_address
        self.assertFalse(
            check_auth(
                claim=mock_nonce_2,
                signed_claim=mock_signed_nonce_2,
                address=mock_addr_2,
            )
        )


if __name__ == "__main__":
    unittest.main()
