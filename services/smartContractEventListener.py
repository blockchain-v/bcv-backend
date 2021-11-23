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

        self.__event_listen([register_filter, unregister_filter, deployVNF, deleteVNF, modifyVNF, reg, unreg])

    def __handle_event(self, event) -> None:
        """
        matches and calls function based on event type
        :param event: event
        :return: None
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
            self.vnfService.deployVNF(event.args.creator, event.args.deploymentId, event.args.vnfdId,
                                      event.args.parameters)
        elif evt == EventTypes.DELETEVNF.name:
            self.vnfService.deleteVNF(event.args.creator, event.args.deploymentId, event.args.vnfId)
        elif evt == EventTypes.MODIFYVNF.name:
            self.vnfService.modifyVNF(event.args.creator, event.args.vnfId, event.args.parameters)
        else:
            print('???')

    def __event_loop(self, event_filter, poll_interval) -> None:
        """
        gets new events based on the type of event this thread is listening to
        :param event_filter:
        :param poll_interval: int
        :return: None
        """
        while True:
            for event in event_filter.get_new_entries():
                self.__handle_event(event)
            time.sleep(poll_interval)

    def __event_listen(self, event_filters) -> None:
        """
        Starts a thread for each of the event filters to listen
        :param event_filters: list
        :return: None
        """
        poll_interval = 5
        for event in event_filters:
            worker = Thread(target=self.__event_loop, args=(event, poll_interval), daemon=True)
            worker.start()
