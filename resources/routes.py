from .tackerAPI import TackerVNFDSAPI
from .challengeAPI import ChallengeAPI

def init_routes(api):
    """
    initialize the api routes
    :param api:
    :return:
    """
    api.add_resource(TackerVNFDSAPI, '/api/tacker/vnfds')
    api.add_resource(ChallengeAPI, '/api/challenge')
