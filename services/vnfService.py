from .smartContractService import reportVNFDeployment

class VNFService:

    def __init__(self, tackerClient):
        self.tackerClient = tackerClient

    def deployVNF(self, creator, vnfId, vnfdId, parameters) -> None:
        # TODO call contract with if failed or errored
        try:
            print(creator, vnfId, vnfdId, parameters)
            response = self.tackerClient.create_vnf(vnfdId, parameters)
            success = response.status_code == 201
            data = response.json()

            reportVNFDeployment(creator, data['vnf']['id'],success, '1234' )
        except Exception as e:
            print('e',e)
            reportVNFDeployment(creator, '', False, '1234')

    def deleteVNF(self, creator, vnfId) -> None:
        # TODO call contract with if failed or errored
        print(creator, vnfId)

    def modifyVNF(self, creator, vnfId, parameters) -> None:
        print(creator, vnfId, parameters)
