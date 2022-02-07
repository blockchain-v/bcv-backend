from flask import Response
from openapi_server.tacker import tacker


class VNFDService:
    def __init__(self, tacker_client):
        self.tackerClient = tacker_client

    def get_vnfd(self, vnfd_id):
        try:
            return self.tackerClient.get_vnfd(vnfd_id)
        except:
            return Response(status=400)

    def delete_vnfd(self, vnfd_id):
        try:
            status_code = self.tackerClient.delete_vnfd(vnfd_id)
            return Response(status=status_code)
        except:
            return Response(status=400)

    def get_vnfds(self):
        try:
            return self.tackerClient.get_vnfds()
        except:
            return Response(status=400)

    def create_vnfd(self, new_vnfd=None):
        try:
            attributes = new_vnfd.attributes
            name = new_vnfd.name
            description = new_vnfd.description
            res, status_code = self.tackerClient.create_vnfd(attributes, name, description)
            return res, status_code
        except:
            return Response(status=400)


service = VNFDService(tacker_client=tacker)
