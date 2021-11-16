class VNFService:

    def __init__(self, tackerClient):
        self.tackerClient = tackerClient

    def deployVNF(self, creator, vnfId, vnfdId, parameters) -> None:
        # TODO call contract with if failed or errored
        print(creator, vnfId, vnfdId, parameters)
        self.tackerClient.create_vnf(vnfdId, parameters)

    def deleteVNF(self, creator, vnfId) -> None:
        # TODO call contract with if failed or errored
        print(creator, vnfId)

    def modifyVNF(self, creator, vnfId, parameters) -> None:
        print(creator, vnfId, parameters)
