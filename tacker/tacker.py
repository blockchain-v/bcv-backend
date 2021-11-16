from config import TACKER_CONFIG
import requests


class Tacker:
    """
    Tacker's responsibility is to communicate with the Tacker VM
    """

    def __init__(self):
        self.token, self.tenant_id = self.__get_token_scoped()
        self.headers = {'X-Auth-Token': self.token, 'content-type': 'Application/JSON'}
        self.vimId = self.get_vims()[0]['id']
        print('vimId', self.vimId)

    def __get_token_scoped(self) -> object:
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
                                "id": TACKER_CONFIG['USER_ID'],
                                "password": TACKER_CONFIG['PASSWORD']
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

            response = requests.post(f"{TACKER_CONFIG['AUTH_URL']}/tokens", json=data,
                                     headers={'content-type': 'Application/JSON'})
            token = response.headers['X-Subject-Token']
            catalog = response.json().get('token').get('catalog')
            tenant_id = next(x for x in catalog if x['name'] == 'keystone').get('id')
            return token, tenant_id
        except Exception as e:
            print('e', e)

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
        response = requests.get(f"{TACKER_CONFIG['BASEURL']}vims",
                                headers=self.headers)
        vims = response.json().get('vims')
        print('vims: ', vims)
        return vims

    """
    ------------------------
    VNFD (VNF DESCRIPTORS)
    ------------------------
    """

    def get_vnfds(self):
        response = requests.get(f"{TACKER_CONFIG['BASEURL']}vnfds",
                                headers=self.headers)
        vnfs = response.json().get('vnfds')
        print('vnfds: ', vnfs)
        return vnfs

    def get_vnfd(self, vnfdId):
        response = requests.get(f"{TACKER_CONFIG['BASEURL']}vnfds/{vnfdId}",
                                headers=self.headers)
        vnfd = response.json().get('vnfd')
        print('vnfs: ', vnfd)
        return vnfd

    def create_vnfd(self, attributes):
        data = {
            "vnfd": {
                "tenant_id": self.tenant_id,
                "name": "vnfd-sample test 3",
                "description": "Sample",
                "service_types": [
                    {
                        "service_type": "vnfd"
                    }
                ],
                "attributes": {}
            }
        }
        data['vnfd']['attributes'] = attributes
        print('data: ', data)

        response = requests.post(f"{TACKER_CONFIG['BASEURL']}vnfds",
                                 headers=self.headers, json=data)
        print('res', response)
        return response

    def delete_vnfd(self, vnfdId):
        response = requests.delete(f"{TACKER_CONFIG['BASEURL']}vnfds/{vnfdId}",
                                   headers=self.headers)
        print('res', response)
        return response

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
        response = requests.get(f"{TACKER_CONFIG['BASEURL']}vnfs",
                                headers=self.headers)
        vnfs = response.json().get('vnfs')
        print('vnfs: ', vnfs)
        return vnfs

    def create_vnf(self, vnfdId, parameters):
        # TODO update properties
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

        response = requests.post(f"{TACKER_CONFIG['BASEURL']}vnfs",
                                 headers=self.headers, json=data)
        print(response)
        return response

    def delete_vnf(self, vnfId):
        # TODO check
        data = {
            "vnf": {
                "attributes": {
                    "force": True
                }
            }
        }
        response = requests.delete(f"{TACKER_CONFIG['BASEURL']}vnfs/{vnfId}",
                                   headers=self.headers)
        print(response)
        return response


tackerClient = Tacker()
