from contract.w3 import w3


def registerBackend(contract):
    """
    Calls the smart contract function 'registerBackend'
    :param contract:
    :return:
    """
    try:
        tx_hash = contract.functions.registerBackend('0x6fBa78085BbD09475723F53C7f3895dBb4b17BC9').transact(
            {"from": "0x474F1243F1Eec4eDfD576425f581Ec1cE3d0A099"})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print('t', tx_receipt)
    except Exception as e:
        print('e', e)
