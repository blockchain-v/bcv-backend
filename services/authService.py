from contract import w3
from uuid import uuid4
from models import Token
from datetime import datetime
from flask import request, abort


def checkAuth(claim, signedString, isAddress=True) -> bool:
    """
    Verifies a claim (e.g. an address) by comparing it to its value that was recovered from a digitally signed string
    :param claim:
    :param signedString:
    :param isAddress:
    :return: boolean
    """
    try:
        # use same hashfunction as in contract to hash the userAddress
        signedAddress = w3.solidityKeccak(['address'], [claim])
        # using the signature, recover the address from the hash
        # this is done to check whether the digital signature was issued by the claimed userAddress

        address = w3.eth.account.recoverHash(signedAddress, signature=signedString)
        return claim == address
    except Exception as e:
        return False


def verifyToken(token):
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


def createToken(value, signedValue):
    try:
        if checkAuth(value, signedValue, isAddress=False):
            tokenValue = uuid4().hex
            newToken = Token(value=tokenValue)
            newToken.save()
            return tokenValue
        else:
            return False
    except Exception as e:
        return False


def auth(func):
    def wrapper(*args, **kwargs):

        token = request.headers.get('Authentication')
        val = verifyToken(token)
        if val:
            return func(*args, **kwargs)
        else:
            return abort(401)


    return wrapper
