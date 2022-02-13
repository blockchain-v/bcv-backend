import json
from openapi_server.config import TACKER_CONFIG
import requests
import logging
from openapi_server.models import TackerConfig
from openapi_server.nvf_framework.nfv_framework import AbstractNFVFramework

log = logging.getLogger("tacker")


class Tacker(AbstractNFVFramework):
    """
    Tacker's responsibility is to communicate with the Tacker instance running on the VM
    """

    def __init__(self, tacker_config):
        self._tacker_config = tacker_config
        # note: only after calling the function 'connect', the object is completely initialized

    def connect(self):
        token, self._tenant_id = self._get_token()
        super().__init__(token=token, base_url=self._tacker_config.base_url)

        self._vim_id = self._get_vim_id()

    def _get_token(self):
        return self._get_token_scoped()

    def _get_token_scoped(self):
        """
        Gets a scoped authentication token and tenant_id from Tacker
        :return:
        :rtype: str
        """
        try:
            data = {
                "auth": {
                    "identity": {
                        "methods": ["password"],
                        "password": {
                            "user": {
                                "id": self._tacker_config.user_id,
                                "password": self._tacker_config.pw,
                            }
                        },
                    },
                    "scope": {"system": {"all": True}},
                }
            }

            response = requests.post(
                f"{self._tacker_config.auth_url}/tokens",
                json=data,
                headers={"content-type": "Application/JSON"},
            )
            token = response.headers["X-Subject-Token"]
            catalog = response.json().get("token").get("catalog")
            tenant_id = next(x for x in catalog if x["name"] == "keystone").get("id")
            return token, tenant_id
        except Exception as e:
            log.info(f"e: {e}")

    def _get_vim_id(self):
        vim_ids, _ = self.get_vims()
        log.info(f"vims: {vim_ids}")
        return vim_ids[0]["id"]

    """
    ------------------------
    VIMS
    ------------------------
    """

    def get_vims(self):
        """
        Returns VIMS from tacker
        :return:
        """
        response = self._reqGET("vims")
        vims = response.json().get("vims")
        return vims, response.status_code

    """
    ------------------------
    VNFD (VNF DESCRIPTORS)
    ------------------------
    """

    def get_vnfds(self):
        """
        Returns all vnfd's
        """
        response = self._reqGET("vnfds")
        vnfds = response.json().get("vnfds")
        return vnfds, response.status_code

    def get_vnfd(self, vnfd_id):
        """
        Returns a vnfd by its id
        :param vnfd_id: str
        """
        response = self._reqGET(f"vnfds/{vnfd_id}")
        vnfd = response.json().get("vnfd")
        return vnfd, response.status_code

    def create_vnfd(self, attributes, name, description):
        """
        Create a vnfd in tacker
        :param attributes: dict
        :param name: str
        :param description: str
        """
        data = {
            "vnfd": {
                "tenant_id": self._tenant_id,
                "service_types": [{"service_type": "vnfd"}],
                "attributes": {},
            }
        }
        data["vnfd"]["attributes"] = attributes
        data["vnfd"]["name"] = name
        data["vnfd"]["description"] = description

        response = self._reqPOST("vnfds", data)
        if not response.json().get("vnfd"):
            return {"Error": response.text}, response.status_code
        return response.json().get("vnfd"), response.status_code

    def delete_vnfd(self, vnfd_id) -> int:
        """
        Deletes a vnfd by its id
        Returns status code upon deletion of a vnfd
        :param vnfd_id: str
        :return: int
        """
        response = self._reqDELETE(f"vnfds/{vnfd_id}")
        log.info(f"res {response}")
        return response.status_code

    """
    ------------------------
    VNFS
    ------------------------
    """

    def get_vnfs(self):
        """
        Returns VNFS from tacker
        :return:
        """
        response = self._reqGET("vnfs")
        vnfs = response.json().get("vnfs")
        return vnfs, response.status_code

    def get_vnf(self, vnf_id):
        """
        Returns a VNF from tacker
        :return:
        """
        response = self._reqGET(f"vnfs/{vnf_id}")
        vnf = response.json().get("vnf")
        return vnf, response.status_code

    def create_vnf(self, parameters, vnfd_id, *args, **kwargs):
        """
        Create a vnf with the given parameters in tacker.
        :param parameters: str
        :param vnfd_id: str
        """
        parameters = json.loads(parameters)
        data = {
            "vnf": {
                "tenant_id": self._tenant_id,
                "vnfd_id": vnfd_id,
                "vim_id": self._vim_id,
                "placement_attr": {"region_name": "RegionOne"},
            }
        }
        data["vnf"]["attributes"] = parameters.get("attributes")
        data["vnf"]["name"] = parameters.get("name")
        data["vnf"]["description"] = parameters.get("description")

        response = self._reqPOST("vnfs", data)
        log.info(f"{response}")
        if not response.json().get("vnf"):
            return json.loads(response.text), response.status_code
        return response.json().get("vnf"), response.status_code

    def delete_vnf(self, vnf_id):
        """
        Deleted a VNF with the given vnf_id
        :param vnf_id: string
        :return:
        """
        response = self._reqDELETE(f"vnfs/{vnf_id}")
        log.info(f"{response}")
        return response.status_code


tacker_client = Tacker(TackerConfig.from_dict(TACKER_CONFIG))
