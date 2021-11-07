import time
from web3 import Web3
from threading import Thread
from services.registerHandler import register


def start_event_listen(contract):
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
    _event_listen([register_filter, unregister_filter, deployVNF, deleteVNF, modifyVNF])


def _handle_event(event):
    print(Web3.toJSON(event))
    evt = event.event
    # dependencies require py=3.8.*, so no match/case possible
    if evt == 'Register':
        register(event.args.user, event.args.signedAddress)
    elif evt == 'Unregister':
        print('Unregister')
    elif evt == 'DeployVNF':
        print('DeployVNF')
    elif evt == 'DeleteVNF':
        print('DeleteVNF')
    elif evt == 'ModifyVNF':
        print('ModifyVNF')
    else:
        print('???')


def _log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            _handle_event(event)
        time.sleep(poll_interval)


def _event_listen(event_filters):
    for event in event_filters:
        worker = Thread(target=_log_loop, args=(event, 5), daemon=True)
        worker.start()
