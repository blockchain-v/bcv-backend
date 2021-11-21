from .tackerAPI import TackerVNFDSAPI
from .tokenAPI import TokenAPI


def init_routes(api):
    """
    initialize the api routes
    :param api:
    :return:
    """
    api.add_resource(TackerVNFDSAPI, '/api/tacker/vnfds')
    api.add_resource(TokenAPI, '/api/token')
