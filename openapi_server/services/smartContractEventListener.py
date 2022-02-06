import time
from threading import Thread
from .userService import register, unregister
from .vnfService import VNFService
from openapi_server.tacker import tacker
from openapi_server.contract import contract, w3
from enum import Enum, auto
import logging

log = logging.getLogger('smartContractEventListener')


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

    def __init__(self, contract, tacker_client):
        self.contract = contract
        self.vnfService = VNFService(tacker_client)
        self._start_event_listen(self.contract)

    def _start_event_listen(self, contract):
        """
        Starts smart contract event listening service
        :param contract: object
        :return:
        """
        register_filter = contract.events.Register.createFilter(fromBlock='latest')
        unregister_filter = contract.events.Unregister.createFilter(fromBlock='latest')
        deploy_vnf_filter = contract.events.DeployVNF.createFilter(fromBlock='latest')
        delete_vnf_filter = contract.events.DeleteVNF.createFilter(fromBlock='latest')
        # TODO remove registration / unregistering status. Just for testing purposes right now.
        registration_status_filter = contract.events.RegistrationStatus.createFilter(fromBlock='latest')
        unregistering__status_filter = contract.events.UnregistrationStatus.createFilter(fromBlock='latest')

        self._event_listen(
            [register_filter, unregister_filter, deploy_vnf_filter, delete_vnf_filter, registration_status_filter,
             unregistering__status_filter])

    def _handle_event(self, event) -> None:
        """
        matches and calls function based on event type
        :param event: event
        :return: None
        """
        log.info(f'{w3.toJSON(event)}')
        evt = str(event.event).upper()
        log.info(f'evt {evt}')
        # dependencies require py=3.8.*, so no match/case possible
        if evt == EventTypes.REGISTER.name:
            register(event.args.user, event.args.signedAddress)
        elif evt == EventTypes.UNREGISTER.name:
            unregister(event.args.user)
        elif evt == EventTypes.DEPLOYVNF.name:
            self.vnfService.deploy_vnf(event.args.creator, event.args.deploymentId, event.args.vnfdId,
                                       event.args.parameters)
        elif evt == EventTypes.DELETEVNF.name:
            self.vnfService.delete_vnf(event.args.creator, event.args.deploymentId, event.args.vnfId)
        else:
            log.info('???')

    def _event_loop(self, event_filter, poll_interval) -> None:
        """
        gets new events based on the type of event this thread is listening to
        :param event_filter:
        :param poll_interval: int
        :return: None
        """
        while True:
            for event in event_filter.get_new_entries():
                self._handle_event(event)
            time.sleep(poll_interval)

    def _event_listen(self, event_filters) -> None:
        """
        Starts a thread for each of the event filters to listen
        :param event_filters: list
        :return: None
        """
        poll_interval = 5
        for event in event_filters:
            worker = Thread(target=self._event_loop, args=(event, poll_interval), daemon=True)
            worker.start()


eventListener = SmartContractEventListener(contract, tacker)
