import json
from flask import Response, request
from flask_restful import Resource
from tacker import tacker


class TackerVNFDSAPI(Resource):
    def __init__(self):
        self.tackerClient = tacker

    def get(self):
        # TODO handle auth
        return Response(json.dumps({"vnfds": self.tackerClient.get_vnfds()}), mimetype='application/json', status=200)

    def post(self):
        #TODO handle auth
        attributes = request.get_json().get('attributes')
        res = self.tackerClient.create_vnfd(attributes)
        return Response(res, res.status_code)

    def delete(self):
        #TODO handle auth
        vnfdId = request.get_json().get('vnfdId')
        res = self.tackerClient.delete_vnfd(vnfdId)
        return Response(res, res.status_code)