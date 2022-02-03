import logging
import json
from flask import Response
from uuid import uuid4
from openapi_server.services import userRegistered, checkAuth
from openapi_server.repositories import Token, Nonce

log = logging.getLogger('werkzeug')


class TokenService:

    @staticmethod
    def create_nonce(address_request):
        nonce = TokenService.createNonceHandler(address_request.address)
        if nonce:
            return Response(json.dumps({"nonce": nonce}), mimetype='application/json', status=200)
        else:
            return Response(mimetype='application/json', status=403)

    @staticmethod
    def create_token(token_request):
        signedNonce = token_request.signed_nonce
        nonce = token_request.nonce
        address = token_request.address
        isRegistered = userRegistered(address)
        if not isRegistered:
            return Response(json.dumps({"token": None, "isRegistered": isRegistered}), mimetype='application/json',
                            status=204)
        token = TokenService.createTokenHandler(nonce, signedNonce, address)
        if token:
            return Response(json.dumps({"token": token, "isRegistered": isRegistered}), mimetype='application/json',
                            status=200)
        else:
            return Response(mimetype='application/json', status=403)

    @staticmethod
    def createTokenHandler(nonce, signedNonce, address):
        """
        Creates and returns new token for a user if the passed nonce is valid
        :param nonce: string
        :param signedNonce: string
        :param address: string
        :return: token : string
        """
        try:
            if checkAuth(claim=nonce, signedClaim=signedNonce, address=address):
                # delete previous tokens from this user
                Token.objects(userAddress=address).delete()
                # create new token
                tokenValue = uuid4().hex
                newToken = Token(value=tokenValue, userAddress=address)
                newToken.save()
                return tokenValue
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def createNonceHandler(address):
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


service = TokenService()
