from config import TACKER_CONFIG
import requests


class Tacker:

    def __init__(self):
        self.token = self._get_token()
        self.headers = {'X-Auth-Token': self.token}

    def _get_token(self):
        """
        Gets authentication token from Tacker
        :rtype: str
        """
        data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": TACKER_CONFIG['USERNAME'],
                            "domain": {
                                "name": "Default"
                            },
                            "password": TACKER_CONFIG['PASSWORD']
                        }
                    }
                }
            }
        }

        response = requests.post(f"{TACKER_CONFIG['AUTH_URL']}/tokens", json=data,
                                 headers={'content-type': 'Application/JSON'})
        return response.headers['X-Subject-Token']

    def get_vims(self):
        """
        Returns VIMS from tacker
        :return:
        """
        response = requests.get(f"{TACKER_CONFIG['baseurl']}vims",
                                headers=self.headers)
        vims = response.json().get('vims')
        print('vims: ', vims)
        return vims

    def get_vnfs(self):
        """
        Returns VNFS from tacker
        :return:
        """
        response = requests.get(f"{TACKER_CONFIG['baseurl']}vnfs",
                                headers=self.headers)
        vnfs = response.json().get('vnfs')
        print('vnfs: ', vnfs)
        return vnfs
