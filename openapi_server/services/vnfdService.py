from flask import Response
from openapi_server.tacker import tacker


class VNFDService:
    def __init__(self, tackerClient):
        self.tackerClient = tackerClient

    def get_vnfd(self, vnfd_id):
        try:
            return self.tackerClient.get_vnfd(vnfd_id)
        except Exception:
            return Response(status=400)

    def delete_vnfd(self, vnfd_id):
        try:
            status_code = self.tackerClient.delete_vnfd(vnfd_id)
            return Response(status=status_code)
        except Exception:
            return Response(status=400)

    def get_vnfds(self):
        try:
            return self.tackerClient.get_vnfds()
        except Exception:
            return Response(status=400)

    def create_vnfd(self, new_vnfd=None):
        try:
            attributes = new_vnfd.attributes
            name = new_vnfd.name
            description = new_vnfd.description
            res, status_code = self.tackerClient.create_vnfd(attributes, name, description)
            return res, status_code
        except Exception:
            return Response(status=400)


service = VNFDService(tackerClient=tacker)
