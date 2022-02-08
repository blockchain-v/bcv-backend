from openapi_server.services import smartContractService

from openapi_server.nvf_framework import tacker
from openapi_server.models import ContractVNF
import logging
from operator import itemgetter
from ..utils.util import remove_none_entries_from_list

log = logging.getLogger("vnfService")


class VNFService:
    def __init__(self, tacker_client):
        self.tackerClient = tacker_client

    def deploy_vnf(self, event_args_dict) -> None:
        try:
            creator_address, deployment_id, vnfd_id, parameters = itemgetter(
                "creator", "deploymentId", "vnfdId", "parameters"
            )(event_args_dict)
            log.info(f"{creator_address}, {deployment_id}, {vnfd_id}, {parameters}")
            vnf, status_code = self.tackerClient.create_vnf(
                parameters=parameters, vnfd_id=vnfd_id
            )
            success = status_code == 201
            smartContractService.service.report_vnf_deployment(
                deployment_id, creator_address, success, vnf["id"]
            )

        except Exception as e:
            log.info(f" deployVNF error {e}")
            smartContractService.service.report_vnf_deployment(
                deployment_id, creator_address, False, ""
            )

    def delete_vnf(self, event_args_dict) -> None:
        creator_address, deployment_id, vnf_id = itemgetter(
            "creator", "deploymentId", "vnfId"
        )(event_args_dict)
        log.info(f"{creator_address}, {deployment_id}")
        try:
            status_code = self.tackerClient.delete_vnf(vnf_id)
            success = status_code == 204
            smartContractService.service.report_vnf_deletion(
                deployment_id, creator_address, success
            )

        except Exception as e:
            log.info(f" deleteVNF error {e}")
            smartContractService.service.report_vnf_deletion(
                deployment_id, creator_address, False
            )

    def get_users_vnf(self, address, vnf_id=None):
        """
        Returns all vnf details for a specific user
        :param address: string
        :param vnf_id: string
        :return: array | object
        """
        try:
            log.info(f"address {address}")
            # contract_vnf_details = get_vnf_details_from_contract(address)
            # map to ContractVNF model
            contract_vnfs = [
                ContractVNF.from_dict(vnf)
                for vnf in smartContractService.service.get_vnf_details_from_contract(
                    address
                )
            ]
            vnf_details = [
                self.get_vnf_details(vnf)
                for vnf in contract_vnfs
                if vnf.vnf_id and not vnf.is_deleted
            ]
            if not vnf_id:
                return remove_none_entries_from_list(vnf_details)
            return next(
                vnf
                for vnf in remove_none_entries_from_list(vnf_details)
                if vnf.get("id") == vnf_id
            )

        except Exception as e:
            status = 404 if (vnf_id and len(vnf_details) >= 0) else 400
            log.warning(e)
            return "Error", status

    def get_vnf_details(self, contract_vnf):
        """
        Gets vnf details and adds the contract internal's deploymentID as an attribute
        :param contract_vnf: ContractVNF
        """
        res, status = self.tackerClient.get_vnf(contract_vnf.vnf_id)
        if status == 200:
            return {**res, "deploymentID": contract_vnf.deployment_id}
        return


service = VNFService(tacker_client=tacker)
