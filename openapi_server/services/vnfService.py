from flask import Response
from .smartContractService import reportVNFDeployment, reportVNFDeletion, getVnfs
from openapi_server.tacker import tacker
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

    # def modifyVNF(self, creator, vnfId, parameters) -> None:
    #     # TODO: contract function not implemented yet

    def getUsersVNF(self, address, vnfID=None):
        """
        Returns all vnf details for a specific user
        :param token: string
        :param vnfID: string
        :return: array | object
        """
        try:
            log.info(f'address {address}')
            vnfIDs = getVnfs(address)
            vnfDetails = [self.getVNFDetails(e[2], e[0]) for e in vnfIDs if e[2]]
            if not vnfID:
                return vnfDetails
            return next(vnf for vnf in vnfDetails if vnf["id"] == vnfID)

        except Exception:
            status = 404 if (vnfID and len(vnfDetails) >= 0) else 400
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
        return {}


service = VNFService(tackerClient=tacker)
