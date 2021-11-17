import time
from web3 import Web3
from threading import Thread
from services.userService import register, unregister
from enum import Enum, auto
from services.vnfService import VNFService


class EventTypes(Enum):
    """
    Smart Contract Event Types that are listened to by the backend
    """
    REGISTER = auto()
    UNREGISTER = auto()
    DEPLOYVNF = auto()
    DELETEVNF = auto()
    MODIFYVNF = auto()


class SmartContractEventListener:
    """
    This class is responsible for Event listening of smart contract events,
    it calls the appropriate functions depending on the event
    """

    def __init__(self, contract, tackerClient):
        self.contract = contract
        self.vnfService = VNFService(tackerClient)
        self.start_event_listen(self.contract)

    def start_event_listen(self, contract):
        """
        Starts smart contract event listening service
        :param contract: object
        :return:
        """
        register_filter = contract.events.Register.createFilter(fromBlock='latest')
        unregister_filter = contract.events.Unregister.createFilter(fromBlock='latest')
        deployVNF = contract.events.DeployVNF.createFilter(fromBlock='latest')
        deleteVNF = contract.events.DeleteVNF.createFilter(fromBlock='latest')
        modifyVNF = contract.events.ModifyVNF.createFilter(fromBlock='latest')
        # TODO remove reg / unreg. Just for testing purposes right now.
        reg = contract.events.RegistrationStatus.createFilter(fromBlock='latest')
        unreg = contract.events.UnregistrationStatus.createFilter(fromBlock='latest')
        self._event_listen([register_filter, unregister_filter, deployVNF, deleteVNF, modifyVNF,reg, unreg])

    def _handle_event(self, event) -> None:
        """
        Checks
        :param event:
        :return:
        """
        print(Web3.toJSON(event))
        evt = str(event.event).upper()
        print('evt', evt)
        # dependencies require py=3.8.*, so no match/case possible
        if evt == EventTypes.REGISTER.name:
            register(event.args.user, event.args.signedAddress)
        elif evt == EventTypes.UNREGISTER.name:
            unregister(event.args.user)
        elif evt == EventTypes.DEPLOYVNF.name:
            self.vnfService.deployVNF(event.args.creator, event.args.vnfId, event.args.vnfdId, event.args.parameters)
        elif evt == EventTypes.DELETEVNF.name:
            self.vnfService.deleteVNF(event.args.creator, event.args.vnfId)
        elif evt == EventTypes.MODIFYVNF.name:
            self.vnfService.modifyVNF(event.args.creator, event.args.vnfId, event.args.parameters)
        else:
            print('???')

    def _log_loop(self, event_filter, poll_interval) -> None:
        while True:
            for event in event_filter.get_new_entries():
                self._handle_event(event)
            time.sleep(poll_interval)

    def _event_listen(self, event_filters) -> None:
        """
        Starts a thread for each of the event filters
        :param event_filters: list
        :return: None
        """
        for event in event_filters:
            worker = Thread(target=self._log_loop, args=(event, 5), daemon=True)
            worker.start()
