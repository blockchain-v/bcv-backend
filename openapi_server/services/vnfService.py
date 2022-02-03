from flask import Response
from .smartContractService import reportVNFDeployment, reportVNFDeletion, getVnfs
from openapi_server.tacker import tacker


class VNFService:

    def __init__(self, tackerClient):
        self.tackerClient = tackerClient

    def deployVNF(self, creatorAddress, deploymentId, vnfdId, parameters) -> None:
        try:
            print(creatorAddress, deploymentId, vnfdId, parameters)
            vnf, status_code = self.tackerClient.create_vnf(vnfdId, parameters)
            success = status_code == 201
            reportVNFDeployment(deploymentId, creatorAddress, success, vnf['id'])

        except Exception as e:
            print('e', e)
            reportVNFDeployment(deploymentId, creatorAddress, False, '')

    def deleteVNF(self, creatorAddress, deploymentId, vnfId) -> None:
        print(creatorAddress, deploymentId)
        try:
            status_code = self.tackerClient.delete_vnf(vnfId)
            success = status_code == 204
            reportVNFDeletion(deploymentId, creatorAddress, success)

        except Exception:
            reportVNFDeletion(deploymentId, creatorAddress, False)

    # def modifyVNF(self, creator, vnfId, parameters) -> None:
    #     # TODO: contract function not implemented yet
    #     print(creator, vnfId, parameters)

    def getUsersVNF(self, address, vnfID=None):
        """
        Returns all vnf details for a specific user
        :param token: string
        :param vnfID: string
        :return: array | object
        """
        try:
            print('address', address)
            vnfIDs = getVnfs(address)
            vnfDetails = [self.tackerClient.get_vnf(e[2])[0] for e in vnfIDs if e[2]]
            if not vnfID:
                return vnfDetails
            return next(x for x in vnfDetails if x["id"] == vnfID)

        except Exception:
            status = 404 if (vnfID and len(vnfDetails) >= 0) else 400
            return Response(mimetype='application/json', status=status)


service = VNFService(tackerClient=tacker)
