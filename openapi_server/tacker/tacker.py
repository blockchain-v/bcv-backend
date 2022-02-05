import json
from config import TACKER_CONFIG
import requests
import logging
from openapi_server.models import TackerConfig

log = logging.getLogger('tacker')


class Tacker:
    """
    Tacker's responsibility is to communicate with the Tacker instance running on the VM
    """

    def __init__(self, tackerConfig):
        self._tackerConfig = tackerConfig
        self.token, self.tenant_id = self._get_token_scoped()
        self._headers = None
        self.vimId = self._get_vimId()

    @property
    def headers(self):
        return {'X-Auth-Token': self.token, 'content-type': 'Application/JSON'}

    @headers.setter
    def headers(self, headers):
        self._headers = headers

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
                        "methods": [
                            "password"
                        ],
                        "password": {
                            "user": {
                                "id": self._tackerConfig.user_id,
                                "password": self._tackerConfig.pw
                            }
                        }
                    },
                    "scope": {
                        "system": {
                            "all": True
                        }
                    }
                }
            }

            response = requests.post(f"{self._tackerConfig.auth_url}/tokens", json=data,
                                     headers={'content-type': 'Application/JSON'})
            token = response.headers['X-Subject-Token']
            catalog = response.json().get('token').get('catalog')
            tenant_id = next(x for x in catalog if x['name'] == 'keystone').get('id')
            return token, tenant_id
        except Exception as e:
            log.info(f'e: {e}')

    def _get_vimId(self):
        vimIds, _ = self.get_vims()
        log.info(f'vims: {vimIds}')
        return vimIds[0]['id']

    def _tackerGET(self, resourceURL):
        return requests.get(f"{self._tackerConfig.base_url}{resourceURL}",
                            headers=self.headers)

    def _tackerPOST(self, resourceURL, data):
        return requests.post(f"{self._tackerConfig.base_url}{resourceURL}",
                             headers=self.headers, json=data)

    def _tackerDELETE(self, resourceURL):
        return requests.delete(f"{self._tackerConfig.base_url}{resourceURL}",
                               headers=self.headers)

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
        response = self._tackerGET('vims')
        vims = response.json().get('vims')
        return vims, response.status_code

    """
    ------------------------
    VNFD (VNF DESCRIPTORS)
    ------------------------
    """

    def get_vnfds(self):
        response = self._tackerGET('vnfds')
        vnfds = response.json().get('vnfds')
        log.info(f'vnfds: {vnfds}')
        return vnfds, response.status_code

    def get_vnfd(self, vnfdId):
        response = self._tackerGET(f'vnfds/{vnfdId}')
        vnfd = response.json().get('vnfd')
        return vnfd, response.status_code

    def create_vnfd(self, attributes, name, description):
        data = {
            "vnfd": {
                "tenant_id": self.tenant_id,
                # "name": "vnfd-sample test 3",
                # "description": "Sample",
                "service_types": [
                    {
                        "service_type": "vnfd"
                    }
                ],
                "attributes": {}
            }
        }
        data['vnfd']['attributes'] = attributes
        data['vnfd']['name'] = name
        data['vnfd']['description'] = description

        response = self._tackerPOST('vnfds', data)
        return response.json().get('vnfd'), response.status_code

    def delete_vnfd(self, vnfdId) -> int:
        """
        Returns status code upon deletion of a vnfd
        :param vnfdId:
        :return:
        """
        response = self._tackerDELETE(f'vnfds/{vnfdId}')
        log.info(f'res {response}')
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
        response = self._tackerGET('vnfs')
        vnfs = response.json().get('vnfs')
        log.info(f'vnfs: {vnfs}')
        return vnfs, response.status_code

    def get_vnf(self, vnfId):
        """
        Returns a VNF from tacker
        :return:
        """
        response = self._tackerGET(f'vnfs/{vnfId}')
        vnf = response.json().get('vnf')
        return vnf, response.status_code

    def create_vnf(self, vnfdId, parameters):
        # TODO update properties
        parameters = json.loads(parameters)
        data = {
            "vnf": {
                "tenant_id": self.tenant_id,
                "vnfd_id": vnfdId,
                "vim_id": self.vimId,
                # "name": "Test VNF 2",
                # "description": "Test VNF 2",
                # "attributes": {
                #     "config": {
                #         "vdus": {
                #             "vdu1": {
                #                 "config": {
                #                     "firewall": "package firewall\n"
                #                 }
                #             }
                #         }
                #     },
                #     "param_values": {
                #         "vdus": {
                #             "vdu1": {
                #                 "param": {
                #                     "vdu-name": "openwrt_vdu1"
                #                 }
                #             }
                #         }
                #     }
                # },
                "placement_attr": {
                    "region_name": "RegionOne"
                }
            }
        }
        data['vnf']['attributes'] = parameters.get('attributes')
        data['vnf']['name'] = parameters.get('name')
        data['vnf']['description'] = parameters.get('description')

        response = self._tackerPOST('vnfs', data)
        log.info(f'{response}')
        return response.json().get('vnf'), response.status_code

    def delete_vnf(self, vnfId):
        """
        Deleted a VNF with the given vnfId
        :param vnfId: string
        :return:
        """
        response = self._tackerDELETE(f'vnfs/{vnfId}')
        log.info(f'{response}')
        return response.status_code


tackerClient = Tacker(TackerConfig.from_dict(TACKER_CONFIG))
# todo remove
tackerClient.get_vims()
tackerClient.get_vnfs()
tackerClient.get_vnfds()
