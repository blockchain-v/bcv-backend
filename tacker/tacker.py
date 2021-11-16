from config import TACKER_CONFIG
import requests


class Tacker:
    """
    Tacker's responsibility is to communicate with the Tacker VM
    """

    def __init__(self):
        self.token, self.tenant_id = self.__get_token_scoped()
        self.headers = {'X-Auth-Token': self.token}

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
    VNF DESCRIPTORS
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

    def create_vnfd(self):
        # TODO change
        data = {
            "vnfd": {
                "tenant_id": TACKER_CONFIG['TACKER_TENANT_ID']},
            "name": "vnfd-sample test 3",
            "description": "Sample",
            "service_types": [
                {
                    "service_type": "vnfd"
                }
            ],
            "attributes": {
                "vnfd": {
                    "tosca_definitions_version": "tosca_simple_profile_for_nfv_1_0_0",
                    "description": "Demo example",
                    "metadata": {
                        "template_name": "sample-tosca-vnfd"
                    },
                    "topology_template": {
                        "node_templates": {
                            "VDU1": {
                                "type": "tosca.nodes.nfv.VDU.Tacker",
                                "capabilities": {
                                    "nfv_compute": {
                                        "properties": {
                                            "num_cpus": 1,
                                            "mem_size": "512 MB",
                                            "disk_size": "1 GB"
                                        }
                                    }
                                },
                                "properties": {
                                    "image": "cirros-0.5.2-x86_64-disk"
                                }
                            },
                            "CP1": {
                                "type": "tosca.nodes.nfv.CP.Tacker",
                                "properties": {
                                    "order": 0,
                                    "management": True,
                                    "anti_spoofing_protection": False
                                },
                                "requirements": [
                                    {
                                        "virtualLink": {
                                            "node": "VL1"
                                        }
                                    },
                                    {
                                        "virtualBinding": {
                                            "node": "VDU1"
                                        }
                                    }
                                ]
                            },
                            "VL1": {
                                "type": "tosca.nodes.nfv.VL",
                                "properties": {
                                    "vendor": "Tacker",
                                    "network_name": "net2"
                                }
                            }
                        }
                    }
                }
            }
        }

        response = requests.post(f"{TACKER_CONFIG['BASEURL']}vnfds",
                                 headers=self.headers, data=data)
        print('res', response)

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

    def create_vnf(self, vnfdId, vimId):
        # TODO update properties
        data = {
            "vnf": {
                "tenant_id": TACKER_CONFIG['TENANT_ID'],
                "vnfd_id": vnfdId,
                "vim_id": vimId,
                "name": "Test VNF 2",
                "description": "Test VNF 2",
                "attributes": {
                    "config": {
                        "vdus": {
                            "vdu1": {
                                "config": {
                                    "firewall": "package firewall\n"
                                }
                            }
                        }
                    },
                    "param_values": {
                        "vdus": {
                            "vdu1": {
                                "param": {
                                    "vdu-name": "openwrt_vdu1"
                                }
                            }
                        }
                    }
                },
                "placement_attr": {
                    "region_name": "RegionOne"
                }
            }
        }

        response = requests.post(f"{TACKER_CONFIG['BASEURL']}vnfs",
                                 headers=self.headers, data=data)
        print(response)

    def delete_vnf(self, vnfId):
        data = {
            "vnf": {
                "attributes": {
                    "force": True
                }
            }
        }
        response = requests.delete(f"{TACKER_CONFIG['BASEURL']}vnfs/{vnfId}",
                                   headers=self.headers, data=data)
        print(response)


tackerClient = Tacker()
