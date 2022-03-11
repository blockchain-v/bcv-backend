import functools

from openapi_server.contract.eventListening.abstractObserver import AbstractObserver
from openapi_server.contract.eventListening.eventListenerSubject import eventListener
from abc import ABC
import logging

log = logging.getLogger("observers")


def log_event(func):
    """
    Decorator to log sc events
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        log.info(f"{self.event} event")
        return func(self, *args, **kwargs)

    # call inner
    return wrapper


class AbstractPolling(ABC):
    """
    Handles polling interval: separate dataclass might be nicer (subtyping)
    """

    def __init__(self, poll_interval):
        self.poll_interval = poll_interval


class RegisterObserver(AbstractObserver, AbstractPolling):
    """
    Observer for registering events
    """

    def __init__(self, observable, user_service, poll_interval=5):
        super().__init__(poll_interval=poll_interval)
        self.event = "Register"
        self.user_service = user_service
        observable.attach(self)

    @log_event
    def update(self, event, *args, **kwargs):
        self.user_service.register(event.args)


class UnregisterObserver(AbstractObserver, AbstractPolling):
    """
    Observer for unregistering events
    """

    def __init__(self, observable, user_service, poll_interval=5):
        super().__init__(poll_interval=poll_interval)
        self.event = "Unregister"
        self.user_service = user_service
        observable.attach(self)

    @log_event
    def update(self, event, *args, **kwargs):
        self.user_service.unregister(event.args)


class DeployVNFObserver(AbstractObserver, AbstractPolling):
    """Observer for vnf deployment events"""

    def __init__(self, observable, vnf_service, poll_interval=5):
        super().__init__(poll_interval=poll_interval)
        self.event = "DeployVNF"
        self.vnf_service = vnf_service
        observable.attach(self)

    @log_event
    def update(self, event, *args, **kwargs):
        self.vnf_service.deploy_vnf(event.args)


class DeleteVNFObserver(AbstractObserver, AbstractPolling):
    """Observer for vnf deletion events"""

    def __init__(self, observable, vnf_service, poll_interval=5):
        super().__init__(poll_interval=poll_interval)
        self.event = "DeleteVNF"
        self.vnf_service = vnf_service
        observable.attach(self)

    @log_event
    def update(self, event, *args, **kwargs):
        self.vnf_service.delete_vnf(event.args)


class RegistrationStatusObserver(AbstractObserver, AbstractPolling):
    """Observer for registration status events"""

    def __init__(self, observable, poll_interval=5):
        super().__init__(poll_interval=poll_interval)
        self.event = "RegistrationStatus"
        observable.attach(self)

    @log_event
    def update(self, event, *args, **kwargs):
        pass


class UnregistrationStatusObserver(AbstractObserver, AbstractPolling):
    """observer for unregistration status events"""

    def __init__(self, observable, poll_interval=5):
        super().__init__(poll_interval=poll_interval)
        self.event = "UnregistrationStatus"
        observable.attach(self)

    @log_event
    def update(self, event, *args, **kwargs):
        pass


def start_sc_event_listening(user_service, vnf_service, *args, **kwargs):
    """
    creates event listener observers objects and by attaching them, starts event listening as well.
    If more events are to be listened for, they should be added here.
    """
    RegisterObserver(eventListener, user_service.service)
    UnregisterObserver(eventListener, user_service.service)
    DeployVNFObserver(eventListener, vnf_service.service)
    DeleteVNFObserver(eventListener, vnf_service.service)
    RegistrationStatusObserver(eventListener)
    UnregistrationStatusObserver(eventListener)
