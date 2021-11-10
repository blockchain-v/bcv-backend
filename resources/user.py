from flask import Response, request
from models.user import User
from flask_restful import Resource


class UsersAPI(Resource):
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype='application/json', status=200)
