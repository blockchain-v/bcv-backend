import logging
from uuid import uuid4
import jwt
from datetime import datetime, timedelta
from mongoengine import DoesNotExist
from openapi_server.contract import w3
from openapi_server import config
from openapi_server.services import userService
from openapi_server.utils import check_auth
from openapi_server.repositories import Nonce

log = logging.getLogger("TokenService")


class TokenService:
    """
    Service class for the token resource
    """

    @staticmethod
    def create_nonce(address_request):
        """
        :param address_request: AddressRequest
        :return: Response
        """
        if not w3.isAddress(address_request.address):
            return "Error", 403
        nonce = TokenService.create_nonce_handler(address_request.address)
        if nonce:
            return {"nonce": nonce}, 201
        else:
            return "Error", 403

    @staticmethod
    def create_token(token_request):
        """
        :param token_request: TokenRequest
        :return: Response
        """
        is_registered = userService.service.is_user_registered(token_request.address)
        if not is_registered:
            return {"isRegistered": False}, 200
        token = TokenService.create_token_handler(
            token_request.nonce, token_request.signed_nonce, token_request.address
        )
        if token:
            # nonce has been consumed
            try:
                nonce_to_delete = Nonce.objects(address=token_request.address)
                nonce_to_delete.delete()
            except DoesNotExist:
                pass
            return {"token": token, "isRegistered": is_registered}, 201
        else:
            return "Error", 403

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
                token = jwt.encode(
                    {
                        "address": address,
                        "exp": datetime.utcnow() + timedelta(hours=24),
                    },
                    config.JWT_SECRET,
                )
                return token
            else:
                return False
        except:
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
            nonce_val = "0x" + uuid4().hex
            new_nonce = Nonce(address=address, value=nonce_val)
            new_nonce.save()
            return nonce_val
        except:
            return False


service = TokenService()
