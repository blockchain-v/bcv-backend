from .user import UsersAPI

def init_routes(api):
    api.add_resource(UsersAPI, '/api/users')