from openapi_server.models.vnf import Vnf  # noqa: E501
from openapi_server.services import errormsgService


def get_errormsg(token_info, vnf_id=None, deployment_id=None):  # noqa: E501
    """Returns errormsg for a vnf deployment_id or vnf_id

    Returns errors for a user, if auth was successful # noqa: E501

    :param token_info: dict
    :param vnf_id: string
    :param deployment_id: int
    """
    return errormsgService.service.get_errormsg(
        vnf_id=vnf_id,
        deployment_id=deployment_id,
        user_address=token_info.get("userAddress"),
    )
