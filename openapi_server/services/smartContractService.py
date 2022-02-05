from openapi_server.contract.w3 import w3, contract
from config import SC_BACKEND_CONFIG
import logging
log = logging.getLogger('smartContractService')


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
        log.info(f'registerBackend receipt {tx_receipt}')
    except Exception as e:
        log.info(f'registerBackend error {e}')


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
        log.info(f'user {user}, success: {success}')
        tx_hash = contract.functions.reportRegistration(user, success).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        log.info(f' transaction receipt: {tx_receipt}')
    except Exception as e:
        log.info(f'reportRegistrationToSC error {e}')


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
        log.info(f'user {user}, success: {success}')
        tx_hash = contract.functions.reportUnregistration(user, success).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        log.info(f' transaction receipt: {tx_receipt}')
    except Exception as e:
        log.info(f'reportUnregistrationToSC error {e}')


def reportVNFDeployment(deploymentId, creatorAddress, success, tackerVNFId):
    """
    Reports whether an attempt to create a VNF has been successful.
    Calls the SC function reportDeployment.
    :param deploymentId: int : SC internal identifier for the VNF
    :param creatorAddress: string: address of the user whom the VNF belongs to
    :param success: bool: signs whether the VNF has been successfully created
    :param tackerVNFId: string: id of the newly created VNF, empty string if unsuccessful
    :return:
    """
    try:
        tx_hash = contract.functions.reportDeployment(deploymentId, creatorAddress, success, tackerVNFId).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        log.info(f' transaction receipt: {tx_receipt}')
    except Exception as e:
        log.info(f'reportVNFDeployment error {e}')


def reportVNFDeletion(deploymentId, creatorAddress, success):
    """
    Reports whether an attempt to delete a VNF has been successful.
    Calls the SC function reportDeletion.
    :param deploymentId: int : SC internal identifier for the VNF
    :param creatorAddress: string: address of the user whom the VNF belonged to
    :param success: bool: signs whether the VNF has been successfully deleted
    :return:
    """
    try:
        tx_hash = contract.functions.reportDeletion(deploymentId, creatorAddress, success).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        log.info(f' transaction receipt: {tx_receipt}')
    except Exception as e:
        log.info(f'reportVNFDeletion error {e}')


def get_vnf_details_from_contract(address):
    """
    Calls the SC function getVnfs to get all vnf details for a specific user.
    :param address:
    :return:
    """
    try:
        return contract.functions.getVnfs(address).call({"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
    except Exception as e:
        log.info(f'getVnfs error {e}')
        return False
