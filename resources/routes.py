from .usersAPI import UsersAPI

def init_routes(api):
    api.add_resource(UsersAPI, '/api/users')
    # api.add_resource(TackerVNFDSAPI(tacker), '/api/tacker/vnfds')