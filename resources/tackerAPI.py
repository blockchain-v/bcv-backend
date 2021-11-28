from flask import Response, request, jsonify
from flask_restful import Resource
from tacker import tacker
from services import auth, VNFService


class TackerVNFDSAPI(Resource):
    def __init__(self):
        self.tackerClient = tacker

    @auth
    def get(self) -> Response:
        """
        Returns all VNFD (vnf descriptors) from the tacker instance, if auth was successful
        :return: Response: 200 if successful
        """
        try:
            return self.tackerClient.get_vnfds()
        except Exception as e:
            return Response(status=400)

    @auth
    def post(self) -> Response:
        """
        Post a new VNFD (vnf descriptor) to the tacker instance, if auth was successful
        :return: 201 if successful
        """
        try:
            attributes = request.get_json().get('attributes')
            name = request.get_json().get('name')
            description = request.get_json().get('description')
            res, status_code = self.tackerClient.create_vnfd(attributes, name, description)
            return res, status_code
        except Exception as e:
            return Response(status=400)


class TackerVNFDAPI(Resource):
    def __init__(self):
        self.tackerClient = tacker

    @auth
    def get(self, vnfdId) -> Response:
        """
        Returns a VNFD (vnf descriptors) from the tacker instance, if auth was successful
        :return: Response: 200 if successful
        """
        try:
            return self.tackerClient.get_vnfd(vnfdId)
        except Exception as e:
            return Response(status=400)

    @auth
    def delete(self, vnfdId) -> Response:
        """
        Delete a VNFD (vnf descriptor) from the tacker instance, if auth was successful
        :return: 204 if successful
        """
        try:
            status_code = self.tackerClient.delete_vnfd(vnfdId)
            return Response(status=status_code)
        except Exception as e:
            return Response(status=400)


class TackerVNFAPI(Resource):
    def __init__(self):
        self.tackerClient = tacker

    @auth
    def get(self, vnfId) -> Response:
        """
        Get a specific vnf id.
        :return: 200 if successful
        """
        try:
            return self.tackerClient.get_vnf(vnfId)
        except Exception as e:
            return Response(status=400)


class TackerVNFSAPI(Resource):
    def __init__(self):
        self.tackerClient = tacker

    @auth
    def get(self) -> Response:
        """
        Gets VNFS from tacker instance for a specific user.
        This is done by calling the contract to get the vnfs for this user and then getting each individually.
        :return: 200 if successful
        """
        try:
            return VNFService(self.tackerClient).getUsersVNF(token=request.headers.get('Authentication'))
        except Exception as e:
            return Response(status=400)
