import connexion
from openapi_server.services import tokenService

from openapi_server.models.address_request import AddressRequest  # noqa: E501
from openapi_server.models.nonce import Nonce  # noqa: E501
from openapi_server.models.token_request import TokenRequest  # noqa: E501
from openapi_server.models.token_response import TokenResponse  # noqa: E501


def create_nonce():  # noqa: E501
    """Creates and returns a new nonce

    Nonces are valid for one day and are used to issue a token. # noqa: E501


    :rtype: Nonce
    """
    if connexion.request.is_json:
        address_request = AddressRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return tokenService.service.create_nonce(address_request)


def create_token():  # noqa: E501
    """Creates and returns a new token. Requires a nonce.

    Tokens are valid for one day and are used for auth. # noqa: E501


    :rtype: TokenResponse
    """
    if connexion.request.is_json:
        token_request = TokenRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return tokenService.service.create_token(token_request)
