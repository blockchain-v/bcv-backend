from contract import w3
from uuid import uuid4
from models import Token, Nonce
from datetime import datetime
from flask import request, abort


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
        return __checkAuthForAddress(claim, signedClaim) if address is None else __checkAuthForNonces(claim,
                                                                                                      signedClaim,
                                                                                                      address)
    except Exception as e:
        return False


def __checkAuthForAddress(claimedAddress, signedString) -> bool:
    """
    Verifies a claimed address by comparing it to its value that was recovered from a digitally signed string
    :param claimedAddress:
    :param signedString:
    :return: boolean
    """
    try:
        # use same hashfunction as in contract to hash the userAddress
        hashedClaim = w3.solidityKeccak(['address'], [claimedAddress])
        address = __recoverAddress(hashedClaim, signedString)
        return claimedAddress == address
    except Exception as e:
        return False


def __checkAuthForNonces(nonce, signedNonce, userAddress) -> bool:
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
        address = __recoverAddress(hashedClaim, signedNonce)
        return address == userAddress
    except Exception as e:
        return False


def __recoverAddress(hashedClaim, signedString) -> str:
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
    except Exception as e:
        return False


def createToken(nonce, signedNonce, address):
    """
    Creates and returns new token for a user if the passed nonce is valid
    :param nonce: string
    :param signedNonce: string
    :param address: string
    :return: token : string
    """
    try:
        if checkAuth(claim=nonce, signedClaim=signedNonce, address=address):
            tokenValue = uuid4().hex
            newToken = Token(value=tokenValue)
            newToken.save()
            return tokenValue
        else:
            return False
    except Exception as e:
        return False


def auth(func):
    """
    Auth decorator for api routes that checks whether the passed authentication token is valid
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):

        token = request.headers.get('Authentication')
        val = verifyToken(token)
        if val:
            return func(*args, **kwargs)
        else:
            return abort(401)

    return wrapper


def createNonce(address):
    """
    Creates and returns new nonce for a user and deletes all previously issued nonces that belonged to that user
    :param address: string
    :return: nonceVal : string : a new nonce
    """
    try:
        Nonce.objects(address=address).delete()
        nonceVal = '0x' + uuid4().hex
        newNonce = Nonce(address=address, value=nonceVal)
        newNonce.save()
        return nonceVal
    except Exception as e:
        return False
