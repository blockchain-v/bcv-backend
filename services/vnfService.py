from .authService import getAddressFromToken
from .smartContractService import reportVNFDeployment, reportVNFDeletion, getVnfs


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

        except Exception as e:
            reportVNFDeletion(deploymentId, creatorAddress, False)

    def modifyVNF(self, creator, vnfId, parameters) -> None:
        # TODO: contract function not implemented yet
        print(creator, vnfId, parameters)

    def getUsersVNF(self, token):
        """
        Returns all vnf details for a specific user
        :param token: string
        :return: array
        """
        try:
            address = getAddressFromToken(token)
            print('address', address)
            vnfs = getVnfs(address)
            return [self.tackerClient.get_vnf(e[2])[0] for e in vnfs if e[2]]
        except Exception as e:
            print('e', e)
            return False
