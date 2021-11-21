from flask import Response, request
from flask_restful import Resource
from services import createToken
import json


class TokenAPI(Resource):
    def post(self):
        """
        :return: string: token
        """
        signedValue = request.get_json().get('signedValue')
        value = request.get_json().get('value')

        token = createToken(value, signedValue)
        if token:
            return Response(json.dumps({"token": token}), mimetype='application/json', status=200)
        else:
            return Response(mimetype='application/json', status=403)
