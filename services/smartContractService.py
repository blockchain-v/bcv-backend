from contract.w3 import w3
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
