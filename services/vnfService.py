from .smartContractService import reportVNFDeployment, reportVNFDeletion


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
