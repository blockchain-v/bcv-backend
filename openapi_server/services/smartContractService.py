from openapi_server.contract.w3 import w3, contract
from openapi_server.config import SC_BACKEND_CONFIG
import logging
log = logging.getLogger('smartContractService')


def register_backend_in_sc(contract):
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
        log.info(f'register_backend error {e}')


def report_registration_to_sc(contract, user, success):
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
        log.info(f'report_registration_to_sc error {e}')


def report_unregistration_to_sc(contract, user, success):
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
        log.info(f'report_unregistration_to_sc error {e}')


def report_vnf_deployment(deployment_id, creator_address, success, tacker_vnf_id):
    """
    Reports whether an attempt to create a VNF has been successful.
    Calls the SC function reportDeployment.
    :param deployment_id: int : SC internal identifier for the VNF
    :param creator_address: string: address of the user whom the VNF belongs to
    :param success: bool: signs whether the VNF has been successfully created
    :param tacker_vnf_id: string: id of the newly created VNF, empty string if unsuccessful
    :return:
    """
    try:
        tx_hash = contract.functions.reportDeployment(deployment_id, creator_address, success, tacker_vnf_id).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        log.info(f' transaction receipt: {tx_receipt}')
    except Exception as e:
        log.info(f'report_vnf_deployment error {e}')


def report_vnf_deletion(deployment_id, creator_address, success):
    """
    Reports whether an attempt to delete a VNF has been successful.
    Calls the SC function reportDeletion.
    :param deployment_id: int : SC internal identifier for the VNF
    :param creator_address: string: address of the user whom the VNF belonged to
    :param success: bool: signs whether the VNF has been successfully deleted
    :return:
    """
    try:
        tx_hash = contract.functions.reportDeletion(deployment_id, creator_address, success).transact(
            {"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        log.info(f' transaction receipt: {tx_receipt}')
    except Exception as e:
        log.info(f'report_vnf_deletion error {e}')


def get_vnf_details_from_contract(address):
    """
    Calls the SC function 'getVnfs' to get all vnf details for a specific user.
    :param address:
    :return:
    """
    try:
        return contract.functions.getVnfs(address).call({"from": SC_BACKEND_CONFIG['SC_BACKEND_ADDRESS']})
    except Exception as e:
        log.info(f'get_vnf_details_from_contract error {e}')
        return False
