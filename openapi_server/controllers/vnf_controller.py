from openapi_server.models.vnf import Vnf  # noqa: E501
from openapi_server.services import vnfService


def get_vnf(vnf_id, token_info):  # noqa: E501
    """Returns vnf details for a specific vnfID

    Returns a VNF from the tacker instance, if auth was successful # noqa: E501

    :param vnf_id: string
    :param token_info: dict
    :rtype: Vnf
    """
    return vnfService.service.get_users_vnf(address=token_info.get('userAddress'), vnfID=vnf_id)


def get_vnfs(token_info):  # noqa: E501
    """Returns all vnf details for a user

    This is done by calling the contract to get the vnfs for this user and then getting each individually, if auth was successful. The user is identified by the Authorization token. # noqa: E501

    :param token_info: dict
    :rtype: List[Vnf]
    """
    return vnfService.service.get_users_vnf(address=token_info.get('userAddress'))
