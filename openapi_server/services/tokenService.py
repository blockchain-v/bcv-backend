import logging
import json
from flask import Response
from uuid import uuid4
import jwt
from datetime import datetime, timedelta
from mongoengine import DoesNotExist

import config
from openapi_server.services import is_user_registered, check_auth
from openapi_server.repositories import Nonce

log = logging.getLogger('werkzeug')


class TokenService:

    @staticmethod
    def create_nonce(address_request):
        """
        :param address_request: AddressRequest
        :return: Response
        """
        nonce = TokenService.create_nonce_handler(address_request.address)
        if nonce:
            return Response(json.dumps({"nonce": nonce}), mimetype='application/json', status=200)
        else:
            return Response(mimetype='application/json', status=403)

    @staticmethod
    def create_token(token_request):
        """
        :param token_request: TokenRequest
        :return: Response
        """
        is_registered = is_user_registered(token_request.address)
        if not is_registered:
            return Response(json.dumps({"token": None, "isRegistered": is_registered}), mimetype='application/json',
                            status=204)
        token = TokenService.create_token_handler(token_request.nonce, token_request.signed_nonce, token_request.address)
        if token:
            # nonce has been consumed
            try:
                nonce_to_delete = Nonce.objects(address=token_request.address)
                nonce_to_delete.delete()
            except DoesNotExist:
                pass

            return Response(json.dumps({"token": token, "isRegistered": is_registered}), mimetype='application/json',
                            status=200)
        else:
            return Response(mimetype='application/json', status=403)

    @staticmethod
    def create_token_handler(nonce, signed_nonce, address):
        """
        Creates and returns new jwt token for a user if the passed nonce is valid
        :param nonce: string
        :param signedNonce: string
        :param address: string
        :return: token : string
        """
        try:
            if check_auth(claim=nonce, signed_claim=signed_nonce, address=address):
                token = jwt.encode({
                    'address': address,
                    'exp': datetime.utcnow() + timedelta(hours=24)
                }, config.JWT_SECRET)
                return token
            else:
                return False
        except Exception:
            return False

    @staticmethod
    def create_nonce_handler(address):
        """
        Creates and returns new nonce for a user and deletes the previously issued nonce that belonged to that user
        :param address: string
        :return: nonceVal : string : a new nonce
        """
        try:
            Nonce.objects(address=address).delete()
            nonce_val = '0x' + uuid4().hex
            new_nonce = Nonce(address=address, value=nonce_val)
            new_nonce.save()
            return nonce_val
        except Exception:
            return False


service = TokenService()
