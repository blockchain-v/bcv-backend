from jwt import InvalidTokenError, ExpiredSignatureError
from mongoengine import DoesNotExist
from openapi_server import config
from openapi_server.contract import w3
from openapi_server.repositories import Nonce, User
from datetime import datetime
from flask import abort
import logging
import jwt

log = logging.getLogger("authService")

"""
Util methods for auth
"""


def check_auth(*args, **kwargs) -> bool:
    """
    Verifies a claim (e.g. an address) by comparing it to its value that was recovered from a digitally signed string
    :return: boolean
    """
    try:
        address = kwargs.get("address")
        claim = kwargs.get("claim")
        signed_claim = kwargs.get("signed_claim")
        return (
            _check_auth_for_address(claim, signed_claim)
            if address is None
            else _check_auth_for_nonce(claim, signed_claim, address)
        )
    except:
        log.info("failed to verify authentication signature")
        return False


def _check_auth_for_address(claimed_address, signed_string) -> bool:
    """
    Verifies a claimed address by comparing it to its value that was recovered from a digitally signed string
    :param claimed_address:
    :param signed_string:
    :return: boolean
    """
    try:
        # use same hash function as in contract to hash the userAddress
        hashed_claim = w3.solidityKeccak(["address"], [claimed_address])
        address = _recover_address(hashed_claim, signed_string)
        return claimed_address == address
    except:
        return False


def _check_auth_for_nonce(nonce, signed_nonce, user_address) -> bool:
    """
    Verifies a claimed nonce by comparing it to its value that was recovered from a digitally signed string
    :param nonce:
    :param signed_nonce:
    :param user_address:
    :return: boolean
    """
    try:
        # match passed nonce, userAddress pair with db entry first
        if not verify_nonce(nonce, user_address):
            return False
        # use the same hash function as in frontend to hash the nonce
        hashed_claim = w3.solidityKeccak(["bytes32"], [nonce])
        address = _recover_address(hashed_claim, signed_nonce)
        return address == user_address
    except:
        return False


def _recover_address(hashed_claim, signed_string) -> str:
    """
    Recovers the address from the hashed_claim using the signature.
    This is done to check whether the digital signature was issued by the claimed userAddress
    :param hashed_claim:
    :param signed_string:
    :return: address : str
    """
    return w3.eth.account.recoverHash(hashed_claim, signature=signed_string)


def verify_nonce(nonce, user_address) -> bool:
    """
    Verifies if a given pair of nonce and userAddress exists and is still valid
    :param nonce:
    :param user_address:
    :return: bool: is the nonce valid
    """
    try:
        nonce_from_db = Nonce.objects.get(value=nonce, address=user_address)
        if nonce_from_db is not None:
            issue_date = nonce_from_db.issueDate
            return abs((datetime.now() - issue_date).days) <= 1
    except DoesNotExist:
        return False


def verify_token(token_str) -> bool:
    """
    Verifies if a given token exists and is still valid
    :param token_str: string
    :return: bool : is the token valid
    """
    try:
        token_data = decode_token(token_str)
        user = User.objects.get(address=token_data["address"])
        return len(user) > 0
    except (InvalidTokenError, ExpiredSignatureError, DoesNotExist):
        return False


def get_address_from_token(token):
    """
    Return address from a token
    :param token: string
    :return: address : string | bool
    """
    try:
        token_data = decode_token(token)
        return token_data["address"]
    except InvalidTokenError:
        return False


def authorize(token):
    """
    Authorizes a user and returns the user address
    :param token: str
    :return: dict
    """
    if not verify_token(token):
        return abort(401)
    user_address = get_address_from_token(token)
    return {"userAddress": user_address}


def decode_token(token_str):
    """
    Decodes JWT token
    :param token_str: string
    :return: token : dict
    """
    return jwt.decode(token_str, config.JWT_SECRET, algorithms=["HS256"])
