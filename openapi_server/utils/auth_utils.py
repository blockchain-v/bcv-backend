from jwt import InvalidTokenError, ExpiredSignatureError
from mongoengine import DoesNotExist
from web3.exceptions import InvalidAddress

from openapi_server import config
from openapi_server.contract import w3
from openapi_server.repositories import Nonce, User
import datetime
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
    :return: bool
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
    This is used for the user registration, where claimed_address represents a user address,
    and signed_string represents the digitally signed user address.
    :param claimed_address:
    :param signed_string:
    :return: bool
    """
    try:
        # use same hash function as in contract to hash the userAddress
        hashed_claim = w3.solidityKeccak(["address"], [claimed_address])
        address = _recover_address(hashed_claim, signed_string)
        return claimed_address == address
    except (InvalidAddress, ValueError) as e:
        log.info(f"check auth for address failed {e}")
        return False


def _check_auth_for_nonce(nonce, signed_nonce, user_address) -> bool:
    """
    Verifies a claimed nonce by comparing it to its value that was recovered from a digitally signed string
    :param nonce:
    :param signed_nonce:
    :param user_address:
    :return: bool
    """
    try:
        # match passed nonce, userAddress pair with db entry first
        if not verify_nonce(nonce, user_address):
            return False
        # use the same hash function as in frontend to hash the nonce
        hashed_claim = w3.solidityKeccak(["bytes32"], [nonce])
        address = _recover_address(hashed_claim, signed_nonce)
        return address == user_address
    except (InvalidAddress, ValueError) as e:
        log.info(f"check auth for nonce failed {e}")
        return False


def _recover_address(hashed_claim, signed_string) -> str:
    """
    Recovers the address from the hashed_claim using the signature.
    This is done to check whether the digital signature was issued by the claimed userAddress
    :param hashed_claim: str
    :param signed_string: str
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
            margin = datetime.timedelta(hours=24)
            now = datetime.datetime.now()
            return now - margin <= issue_date <= now
    except DoesNotExist:
        return False


def verify_token(token_str) -> bool:
    """
    Verifies if a given token exists and is still valid
    :param token_str: str
    :return: bool : is the token valid
    """
    try:
        token_data = decode_token(token_str)
        user = User.objects.get(address=token_data["address"])
        return len(user) > 0
    except (InvalidTokenError, ExpiredSignatureError, DoesNotExist) as e:
        log.info(f"token errored: {e}")
        return False


def get_address_from_token(token):
    """
    Return address from a token
    :param token: str
    :return: address : str | bool
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


def decode_token(token_str, secret=config.JWT_SECRET):
    """
    Decodes JWT token
    :param token_str: str
    :param secret: str: jwt secret that was used for encoding
    :return: token : dict
    """
    return jwt.decode(token_str, secret, algorithms=["HS256"])
