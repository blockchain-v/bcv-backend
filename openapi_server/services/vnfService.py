from flask import Response
from .smartContractService import reportVNFDeployment, reportVNFDeletion, get_vnf_details_from_contract
from openapi_server.tacker import tacker
from openapi_server.models import ContractVNF
import logging

log = logging.getLogger('vnfService')


class VNFService:

    def __init__(self, tackerClient):
        self.tackerClient = tackerClient

    def deployVNF(self, creatorAddress, deploymentId, vnfdId, parameters) -> None:
        try:
            log.info(f'{creatorAddress}, {deploymentId}, {vnfdId}, {parameters}')
            vnf, status_code = self.tackerClient.create_vnf(vnfdId, parameters)
            success = status_code == 201
            reportVNFDeployment(deploymentId, creatorAddress, success, vnf['id'])

        except Exception as e:
            log.info(f' deployVNF error {e}')
            reportVNFDeployment(deploymentId, creatorAddress, False, '')

    def deleteVNF(self, creatorAddress, deploymentId, vnfId) -> None:
        log.info(f'{creatorAddress}, {deploymentId}')
        try:
            status_code = self.tackerClient.delete_vnf(vnfId)
            success = status_code == 204
            reportVNFDeletion(deploymentId, creatorAddress, success)

        except Exception:
            reportVNFDeletion(deploymentId, creatorAddress, False)

    def getUsersVNF(self, address, vnfID=None):
        """
        Returns all vnf details for a specific user
        :param address: string
        :param vnfID: string
        :return: array | object
        """
        try:
            log.info(f'address {address}')
            contract_vnf_ids = get_vnf_details_from_contract(address)
            # map to ContractVNF model
            contract_vnfs = [ContractVNF.from_dict(vnf) for vnf in contract_vnf_ids]
            vnf_details = [self.getVNFDetails(vnf.vnfId, vnf.deploymentId) for vnf in contract_vnfs if vnf.vnfId]
            if not vnfID:
                return vnf_details
            return next(vnf for vnf in vnf_details if vnf.get("id") == vnfID)

        except Exception as e:
            status = 404 if (vnfID and len(vnf_details) >= 0) else 400
            log.warning(e)
            return Response(mimetype='application/json', status=status)

    def getVNFDetails(self, vnfID, deploymentID):
        """
        Gets vnf details and adds the contract internal's deploymentID as an attribute
        :param vnfID: string
        :param deploymentID: string
        """
        res, status = self.tackerClient.get_vnf(vnfID)
        if status == 200:
            return {**res, 'deploymentID': deploymentID}
        return


service = VNFService(tackerClient=tacker)
