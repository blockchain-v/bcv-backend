from flask import Response, request
from flask_restful import Resource
from tacker import tacker


class TackerVNFDSAPI(Resource):
    def __init__(self, tackerClient):
        self.tackerClient = tacker

    def get(self):
        vnfds = self.tackerClient.get_vnfds
        return Response(vnfds, mimetype='application/json', status=200)
