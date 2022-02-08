import connexion

from openapi_server.models.new_vnfd import NewVnfd  # noqa: E501
from openapi_server.models.vnfd import Vnfd  # noqa: E501
from openapi_server.services import vnfdService


def create_vnfd(new_vnfd=None):  # noqa: E501
    """Creates a new vnf descriptor

    Creates a new vnf descriptor, if auth was successful # noqa: E501

    :param new_vnfd: 
    :type new_vnfd: dict | bytes

    :rtype: Vnfd
    """
    if connexion.request.is_json:
        new_vnfd = NewVnfd.from_dict(connexion.request.get_json())  # noqa: E501
    return vnfdService.service.create_vnfd(new_vnfd)


def delete_vnfd(vnfd_id):  # noqa: E501
    """Deletes a vnf descriptor with vnfd_id

    Deletes a VNFD (vnf descriptor) from the nvf_framework instance, if auth was successful # noqa: E501

    :param vnfd_id: string
    :rtype: None
    """
    return vnfdService.service.delete_vnfd(vnfd_id)


def get_vnfd(vnfd_id):  # noqa: E501
    """Returns a vnf descriptor with vnfd_id

    Returns a VNFD (vnf descriptor) from the nvf_framework instance, if auth was successful # noqa: E501

    :param vnfd_id: string
    :rtype: Vnfd
    """
    return vnfdService.service.get_vnfd(vnfd_id)


def get_vnfds():  # noqa: E501
    """Returns all vnf descriptors

    Returns all VNFD (vnf descriptors) from the nvf_framework instance, if auth was successful # noqa: E501


    :rtype: List[Vnfd]
    """
    return vnfdService.service.get_vnfds()
