from flask import Response, request
from flask_restful import Resource
from models import Challenge

class ChallengeAPI(Resource):
    def get(self):
        #TODO
        address = request.args.get('address')
        print('address',address)
        value='asdf'
        challenge = Challenge(address=address, challengeValue=value)
        challenge.save()
        return Response(value, mimetype='application/json', status=200)

    def post(self):
        # TODO
        value = request.get_json().get('value')
        return Response(value, mimetype='application/json', status=200)
