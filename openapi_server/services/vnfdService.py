from openapi_server.nvf_framework import tacker
import logging

log = logging.getLogger("vnfdService")


class VNFDService:
    """
    Service class for the vnfd resource
    """

    def __init__(self, tacker_client):
        self.tacker_client = tacker_client

    def get_vnfd(self, vnfd_id):
        """
        Return a specific vnfd by its vnfd_id
        :param vnfd_id: str
        """
        try:
            return self.tacker_client.get_vnfd(vnfd_id)
        except:
            return "Error", 400

    def delete_vnfd(self, vnfd_id):
        """
        Delete a specific vnfd by its vnfd_id
        :param vnfd_id: str
        """
        try:
            status_code = self.tacker_client.delete_vnfd(vnfd_id)
            return "", status_code
        except:
            return "Error", 400

    def get_vnfds(self):
        """
        Get all vnfd's
        """
        try:
            return self.tacker_client.get_vnfds()
        except Exception as e:
            log.info(f" get vnfds failed {e}")
            return "Error", 400

    def create_vnfd(self, new_vnfd=None):
        """
        Create a new vnfd
        :param new_vnfd: NewVnfd
        """
        try:
            attributes = new_vnfd.attributes
            name = new_vnfd.name
            description = new_vnfd.description
            res, status_code = self.tacker_client.create_vnfd(
                attributes, name, description
            )
            return res, status_code
        except:
            return "Error", 400


service = VNFDService(tacker_client=tacker)
