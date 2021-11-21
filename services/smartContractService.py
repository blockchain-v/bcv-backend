from contract.w3 import w3, contract
from config import SC_BACKEND_CONFIG


def registerBackend(contract):
    """
    Calls the smart contract function 'registerBackend'
    :param contract:
    :return:
    """
    try:
        tx_hash = contract.functions.registerBackend(SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS_FROM']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print('t', tx_receipt)
    except Exception as e:
        print('e', e)


def reportRegistrationToSC(contract, user, success):
    """
    Reports whether the registration process in the backend was successful or not.
    This is done by calling the SC function directly.
    :param contract:
    :param user:
    :param success:
    :return:
    """
    try:
        print('user', user, 'success', success)
        tx_hash = contract.functions.reportRegistration(user, success).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print('t', tx_receipt)
    except Exception as e:
        print('e', e)


def reportUnregistrationToSC(contract, user, success):
    """
    Reports whether the unregister process in the backend was successful or not.
    This is done by calling the SC function directly.
    :param contract:
    :param user:
    :param success:
    :return:
    """
    try:
        tx_hash = contract.functions.reportUnregistration(user, success).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print('t', tx_receipt)
    except Exception as e:
        print('e', e)

def reportVNFDeployment(user, vnfId, success, vnfIdEncrypted):
    try:
        tx_hash = contract.functions.reportDeployment(vnfId, user, success, vnfIdEncrypted).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print('t', tx_receipt)
    except Exception as e:
        print('e', e)
