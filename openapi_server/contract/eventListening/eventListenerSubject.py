import time
from threading import Thread
from openapi_server.contract.eventListening.abstractSubject import AbstractSubject
from openapi_server.contract import contract
import logging

log = logging.getLogger("scListener")


class SmartContractEventListener(AbstractSubject):
    """
    This class is responsible for Event listening of smart contract events.

    Observers attach themselves to this event listener, which creates a thread each for the filtering of events.
    the update function of the affected observer is then called.

    It only follows the observer pattern as a guideline, since notifyObserver is not used,
    as attaching an observer starts event listening immediately, and only a single event is to be updated.

    The Smart Contract Event Listening using threads is based on the example of
    https://web3py.readthedocs.io/en/stable/filters.html#asynchronous-filter-polling
    """

    def __init__(self, sc_contract):
        self.contract = sc_contract
        self._observer = set()

    # AbstractSubject overrides

    def attach(self, observer):
        self._observer.add(observer)
        self._evt_listen(observer)

    def detach(self, observer):
        self._observer.remove(observer)
        worker = observer.worker
        worker.join()

    def notifyObservers(self, *args, **kwargs):
        for o in self._observer:
            o.notify(self, *args, **kwargs)

    # ---------

    def _evt_listen(self, observer):
        event = observer.event
        event_filter = self.contract.events[event].createFilter(fromBlock="latest")
        worker = Thread(
            target=self._event_loop, args=(event_filter, observer), daemon=True
        )
        # store to join later
        observer.worker = worker
        worker.start()

    def _event_loop(self, event_filter, observer) -> None:
        """
        gets new events based on the type of event this thread is listening to
        :param event_filter:
        :param poll_interval: int
        :return: None
        """
        while True:
            for event in event_filter.get_new_entries():
                observer.update(event)
            time.sleep(observer.poll_interval)


eventListener = SmartContractEventListener(sc_contract=contract)
