from openapi_server.contract import w3
from uuid import uuid4
from openapi_server.repositories import Token, Nonce, User
from datetime import datetime
from flask import request, abort
import logging

log = logging.getLogger('authService')


def checkAuth(*args, **kwargs) -> bool:
    """
    Verifies a claim (e.g. an address) by comparing it to its value that was recovered from a digitally signed string
    :param claim:
    :param signedString:
    :param isAddress:
    :return: boolean
    """
    try:
        address = kwargs.get('address')
        claim = kwargs.get('claim')
        signedClaim = kwargs.get('signedClaim')
        return _checkAuthForAddress(claim, signedClaim) if address is None else _checkAuthForNonces(claim,
                                                                                                    signedClaim,
                                                                                                    address)
    except Exception as e:
        log.info("failed to verify authentication signature\n")
        return False


def _checkAuthForAddress(claimedAddress, signedString) -> bool:
    """
    Verifies a claimed address by comparing it to its value that was recovered from a digitally signed string
    :param claimedAddress:
    :param signedString:
    :return: boolean
    """
    try:
        # use same hashfunction as in contract to hash the userAddress
        hashedClaim = w3.solidityKeccak(['address'], [claimedAddress])
        address = _recoverAddress(hashedClaim, signedString)
        return claimedAddress == address
    except Exception as e:
        return False


def _checkAuthForNonces(nonce, signedNonce, userAddress) -> bool:
    """
    Verifies a claimed nonce by comparing it to its value that was recovered from a digitally signed string
    :param nonce:
    :param signedNonce:
    :param userAddress:
    :return: boolean
    """
    try:
        # match passed nonce, userAddress pair with db entry first
        if not verifyNonce(nonce, userAddress):
            return False
        # use the same hashfunction as in frontend to hash the nonce
        hashedClaim = w3.solidityKeccak(['bytes32'], [nonce])
        address = _recoverAddress(hashedClaim, signedNonce)
        return address == userAddress
    except Exception as e:
        return False


def _recoverAddress(hashedClaim, signedString) -> str:
    """
    Rcovers the address from the hashedClaim using the signature.
    This is done to check whether the digital signature was issued by the claimed userAddress
    :param hashedClaim:
    :param signedString:
    :return: address : str
    """
    return w3.eth.account.recoverHash(hashedClaim, signature=signedString)


def verifyNonce(nonce, userAddress) -> bool:
    """
    Verifies if a given pair of nonce and userAddress exists and is still valid
    :param nonce:
    :param userAddress:
    :return: bool: is the nonce valid
    """
    try:
        nonceFromDB = Nonce.objects.get(value=nonce, address=userAddress)
        if nonceFromDB is not None:
            issueDate = nonceFromDB.issueDate
            now = datetime.now()
            return abs((now - issueDate).days) <= 1
    except Exception as e:
        return False


def verifyToken(token) -> bool:
    """
    Verifies if a given token exists and is still valid
    :param token: string
    :return: bool : is the token valid
    """
    try:
        tokenMatch = Token.objects.get(value=token)
        if tokenMatch is not None:
            issueDate = tokenMatch.issueDate
            now = datetime.now()
            return abs((now - issueDate).days) <= 1
        else:
            return False
    except Exception:
        return False


def getAddressFromToken(token) -> str:
    """
    Return address from a token
    :param token: string
    :return: address : string
    """
    try:
        tokenMatch = Token.objects.get(value=token)
        return tokenMatch.userAddress
    except Exception:
        return False


def authorize(token):
    if not verifyToken(token):
        return abort(401)
    userAddress = getAddressFromToken(token)
    return {'userAddress': userAddress}
