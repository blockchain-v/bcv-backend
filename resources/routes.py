from .tackerAPI import TackerVNFDSAPI, TackerVNFAPI, TackerVNFSAPI, TackerVNFDAPI
from .tokenAPI import TokenAPI


def init_routes(api) -> None:
    """
    initialize the api routes
    :param api:
    :return:
    """
    api.add_resource(TackerVNFDSAPI, '/api/tacker/vnfds')
    api.add_resource(TackerVNFDAPI, '/api/tacker/vnfds/<vnfdId>')
    api.add_resource(TokenAPI, '/api/token')
    api.add_resource(TackerVNFAPI, '/api/tacker/vnfs/<vnfId>')
    api.add_resource(TackerVNFSAPI, '/api/tacker/vnfs')
