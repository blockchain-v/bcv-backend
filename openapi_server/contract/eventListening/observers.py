from openapi_server.contract.eventListening.abstractObserver import AbstractObserver
from openapi_server.contract.eventListening.eventListenerSubject import eventListener
import logging

log = logging.getLogger("observers")


class RegisterObserver(AbstractObserver):
    def __init__(self, observable, user_service, poll_interval=5):
        self.event = "Register"
        self.user_service = user_service
        self.poll_interval = poll_interval
        observable.attach(self)

    def update(self, event, *args, **kwargs):
        log.info(f"{self.event} event")
        self.user_service.register(event.args)


class UnregisterObserver(AbstractObserver):
    def __init__(self, observable, user_service, poll_interval=5):
        self.event = "Unregister"
        self.user_service = user_service
        self.poll_interval = poll_interval
        observable.attach(self)

    def update(self, event, *args, **kwargs):
        log.info(f"{self.event} event")
        self.user_service.unregister(event.args)


class DeployVNFObserver(AbstractObserver):
    def __init__(self, observable, vnf_service, poll_interval=5):
        self.event = "DeployVNF"
        self.vnf_service = vnf_service
        self.poll_interval = poll_interval
        observable.attach(self)

    def update(self, event, *args, **kwargs):
        log.info(f"{self.event} event")
        self.vnf_service.deploy_vnf(event.args)


class DeleteVNFObserver(AbstractObserver):
    def __init__(self, observable, vnf_service, poll_interval=5):
        self.event = "DeleteVNF"
        self.vnf_service = vnf_service
        self.poll_interval = poll_interval
        observable.attach(self)

    def update(self, event, *args, **kwargs):
        log.info(f"{self.event} event")
        self.vnf_service.delete_vnf(event.args)


class RegistrationStatusObserver(AbstractObserver):
    def __init__(self, observable, poll_interval=5):
        self.event = "RegistrationStatus"
        self.poll_interval = poll_interval
        observable.attach(self)

    def update(self, event, *args, **kwargs):
        log.info(f"{self.event} event")
        pass


class UnregistrationStatusObserver(AbstractObserver):
    def __init__(self, observable, poll_interval=5):
        self.event = "UnregistrationStatus"
        self.poll_interval = poll_interval
        observable.attach(self)

    def update(self, event, *args, **kwargs):
        log.info(f"{self.event} event")
        pass


def start_sc_event_listening(user_service, vnf_service, *args, **kwargs):
    RegisterObserver(eventListener, user_service.service)
    UnregisterObserver(eventListener, user_service.service)
    DeployVNFObserver(eventListener, vnf_service.service)
    DeleteVNFObserver(eventListener, vnf_service.service)
    RegistrationStatusObserver(eventListener)
    UnregistrationStatusObserver(eventListener)
