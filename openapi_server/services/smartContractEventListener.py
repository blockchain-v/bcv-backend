import time
from threading import Thread
from openapi_server.services.userService import register, unregister
from openapi_server.services.vnfService import VNFService
from openapi_server.nvf_framework import tacker
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

    def __init__(self, contract, tacker_client, filters):
        self.contract = contract
        self.vnfService = VNFService(tacker_client)
        self.filters = filters
        self._start_event_listen()

    def _start_event_listen(self):
        """
        Starts smart contract event listening service
        :param contract: object
        :return:
        """

        cfilters = [self.contract.events[event].createFilter(fromBlock='latest') for event in self.filters]
        self._event_listen(cfilters)

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
            register(event.args)
        elif evt == EventTypes.UNREGISTER.name:
            unregister(event.args)
        elif evt == EventTypes.DEPLOYVNF.name:
            self.vnfService.deploy_vnf(event.args)
        elif evt == EventTypes.DELETEVNF.name:
            self.vnfService.delete_vnf(event.args)
        else:
            log.info('???')


# TODO remove registration / unregistering status. Just for testing purposes right now.
event_filters = ['Register', 'Unregister', 'DeployVNF', 'DeleteVNF', 'RegistrationStatus', 'UnregistrationStatus']
eventListener = SmartContractEventListener(contract, tacker, event_filters)
