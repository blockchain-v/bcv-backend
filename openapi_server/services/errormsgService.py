import logging

from openapi_server.repositories import TackerError
from mongoengine import DoesNotExist

log = logging.getLogger("ErrormsgService")


class ErrormsgService:
    @staticmethod
    def get_errormsg(user_address, vnf_id=None, deployment_id=None):
        """
        Returns a Tacker Error message to the client
        :param user_address: str
        :param vnf_id: str
        :param deployment_id: int
        :return: Response
        """
        try:
            if vnf_id:
                err_msg = TackerError.objects.get(address=user_address, vnf_id=vnf_id)
            elif deployment_id:
                err_msg = TackerError.objects.get(
                    address=user_address, deployment_id=deployment_id
                )
            else:
                return "Not Found", 404
            return err_msg, 200
        except DoesNotExist:
            return "Not Found", 404

    @staticmethod
    def store_errormsg(
        tacker_error=None, vnf_id=None, deployment_id=None, address=None
    ):
        """
        Stores a Tacker Error message into the db
        :param tacker_error: TackerErrorModel
        :param vnf_id: str
        :param deployment_id: int
        :param address: str
        """
        try:
            err_msg = TackerError(
                address=address,
                deployment_id=deployment_id,
                vnf_id=vnf_id,
                type=tacker_error.type,
                detail=tacker_error.detail,
                message=tacker_error.message,
            )
            err_msg.save()
        except Exception as e:
            log.info(f"storing error message failed: {e}")


service = ErrormsgService()
