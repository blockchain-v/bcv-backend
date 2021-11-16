import json
from flask import Response, request
from flask_restful import Resource
from tacker import tacker


class TackerVNFDSAPI(Resource):
    def __init__(self):
        self.tackerClient = tacker

    def get(self):
        #TODO handle auth
        return Response(json.dumps({"vnfds": self.tackerClient.get_vnfds()}), mimetype='application/json', status=200)
