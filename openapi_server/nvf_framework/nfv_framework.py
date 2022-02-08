from abc import ABC, abstractmethod
import requests


class AbstractNFVFramework(ABC):
    """
    Abstract baseclass for a nfv framework with default implementation for header and requests
    """

    def __init__(self, token, base_url):
        self._headers = None
        self._token = token
        self._base_url = base_url

    @property
    def headers(self):
        return {'X-Auth-Token': self.token, 'content-type': 'Application/JSON'}

    @headers.setter
    def headers(self, headers):
        self._headers = headers

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, tk):
        self._token = tk

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @abstractmethod
    def _get_token(self):
        pass

    @abstractmethod
    def get_vnfs(self):
        pass

    @abstractmethod
    def get_vnf(self, vnf_id):
        pass

    @abstractmethod
    def create_vnf(self, parameters, *args, **kwargs):
        """
        args and kwargs for liskov
        """
        pass

    @abstractmethod
    def delete_vnf(self, vnf_id, *args, **kwargs):
        pass

    def _reqGET(self, resource_URL):
        return requests.get(f"{self.base_url}{resource_URL}",
                            headers=self.headers)

    def _reqPOST(self, resource_URL, data):
        return requests.post(f"{self.base_url}{resource_URL}",
                             headers=self.headers, json=data)

    def _reqDELETE(self, resource_URL):
        return requests.delete(f"{self.base_url}{resource_URL}",
                               headers=self.headers)
