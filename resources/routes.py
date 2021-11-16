from .tackerAPI import TackerVNFDSAPI
from .usersAPI import UsersAPI

def init_routes(api):
    """
    initialize the api routes
    :param api:
    :return:
    """
    # api.add_resource(UsersAPI, '/api/users')
    api.add_resource(TackerVNFDSAPI, '/api/tacker/vnfds')
