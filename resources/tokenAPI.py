from flask import Response, request
from flask_restful import Resource
from services import createToken, createNonce, userRegistered
import json


class TokenAPI(Resource):
    def post(self) -> Response:
        """
        Returns a new token if auth successful
        :return: Response
        """

        signedNonce = request.get_json().get('signedNonce')
        nonce = request.get_json().get('nonce')
        address = request.get_json().get('address')

        isRegistered = userRegistered(address)
        if not isRegistered:
            return Response(json.dumps({"token": None, "isRegistered": isRegistered }), mimetype='application/json', status=204)

        token = createToken(nonce, signedNonce, address)
        if token:
            return Response(json.dumps({"token": token, "isRegistered": isRegistered }), mimetype='application/json', status=200)
        else:
            return Response(mimetype='application/json', status=403)

    def put(self) -> Response:
        """
        Creates and returns a new nonce
        :return: Response
        """
        address = request.get_json().get('address')
        nonce = createNonce(address)
        if nonce:
            return Response(json.dumps({"nonce": nonce}), mimetype='application/json', status=200)
        else:
            return Response(mimetype='application/json', status=403)
