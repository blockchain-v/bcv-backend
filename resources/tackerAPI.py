import json
from flask import Response, request, jsonify
from flask_restful import Resource
from tacker import tacker
from services import auth

class TackerVNFDSAPI(Resource):
    def __init__(self):
        self.tackerClient = tacker

    @auth
    def get(self):
        return jsonify({"vnfds":self.tackerClient.get_vnfds()})

    @auth
    def post(self):
        attributes = request.get_json().get('attributes')
        res = self.tackerClient.create_vnfd(attributes)
        return Response(res, res.status_code)

    @auth
    def delete(self):
        vnfdId = request.get_json().get('vnfdId')
        res = self.tackerClient.delete_vnfd(vnfdId)
        return Response(res, res.status_code)


class TackerVNFAPI(Resource):
    def __init__(self):
        self.tackerClient = tacker

    # def get(self):
        # get a specific vnf id