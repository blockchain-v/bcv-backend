from openapi_server.contract.w3 import w3, contract
from openapi_server.config import SC_BACKEND_CONFIG, WEB3_CONFIG
import logging

log = logging.getLogger("smartContractService")


class SmartContractService:
    """
    Service class for the smart contract
    """

    def __init__(self, contract):
        self._contract = contract

    @property
    def contract(self):
        return self._contract

    @contract.setter
    def contract(self, cntr):
        self._contract = cntr

    def register_backend_in_sc(self):
        """
        Calls the smart contract function 'registerBackend'
        :return:
        """
        try:
            nonce = w3.eth.get_transaction_count(
                SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS_FROM"]
            )
            contract = self.contract
            txn = contract.functions.registerBackend(
                SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"]
            ).buildTransaction(
                {
                    "from": SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS_FROM"],
                    "nonce": nonce,
                }
            )
            signed_txn = w3.eth.account.sign_transaction(
                txn, private_key=SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS_FROM_PKEY"]
            )
            w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = w3.toHex(w3.keccak(signed_txn.rawTransaction))
            log.info(f"registerBackend receipt {tx_receipt}")
        except Exception as e:
            log.info(f"register_backend error {e}")

    def report_registration_to_sc(self, user, success):
        """
        Reports whether the registration process in the backend was successful or not.
        This is done by calling the SC function directly.
        :param user: str
        :param success: bool
        :return:
        """
        try:
            nonce = w3.eth.get_transaction_count(
                SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"]
            )
            txn = self.contract.functions.reportRegistration(
                user, success
            ).buildTransaction(
                {
                    "from": SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"],
                    "nonce": nonce,
                }
            )
            signed_txn = w3.eth.account.sign_transaction(
                txn, private_key=SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS_PKEY"]
            )
            w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = w3.toHex(w3.keccak(signed_txn.rawTransaction))

            log.info(f" transaction receipt: {tx_receipt}")
        except Exception as e:
            log.info(f"report_registration_to_sc error {e}")

    def report_unregistration_to_sc(self, user, success):
        """
        Reports whether the unregister process in the backend was successful or not.
        This is done by calling the SC function directly.
        :param user: str
        :param success: bool
        :return:
        """
        try:

            nonce = w3.eth.get_transaction_count(
                SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"]
            )
            txn = self.contract.functions.reportUnregistration(
                user, success
            ).buildTransaction(
                {
                    "from": SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"],
                    "nonce": nonce,
                }
            )
            signed_txn = w3.eth.account.sign_transaction(
                txn, private_key=SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS_PKEY"]
            )
            w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = w3.toHex(w3.keccak(signed_txn.rawTransaction))

            #
            # log.info(f"user {user}, success: {success}")
            # tx_hash = self.contract.functions.reportUnregistration(
            #     user, success
            # ).transact({"from": SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"]})
            # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            log.info(f" transaction receipt: {tx_receipt}")
        except Exception as e:
            log.info(f"report_unregistration_to_sc error {e}")

    def report_vnf_deployment(
        self, deployment_id, creator_address, success, tacker_vnf_id
    ):
        """
        Reports whether an attempt to create a VNF has been successful.
        Calls the SC function reportDeployment.
        :param deployment_id: int : SC internal identifier for the VNF
        :param creator_address: str: address of the user whom the VNF belongs to
        :param success: bool: signs whether the VNF has been successfully created
        :param tacker_vnf_id: str: id of the newly created VNF, empty string if unsuccessful
        :return:
        """
        try:
            tx_hash = self.contract.functions.reportDeployment(
                deployment_id, creator_address, success, tacker_vnf_id
            ).transact({"from": SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"]})
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            log.info(f" transaction receipt: {tx_receipt}")
        except Exception as e:
            log.info(f"report_vnf_deployment error {e}")

    def report_vnf_deletion(self, deployment_id, creator_address, success):
        """
        Reports whether an attempt to delete a VNF has been successful.
        Calls the SC function reportDeletion.
        :param deployment_id: int : SC internal identifier for the VNF
        :param creator_address: str: address of the user whom the VNF belonged to
        :param success: bool: signs whether the VNF has been successfully deleted
        :return:
        """
        try:
            tx_hash = self.contract.functions.reportDeletion(
                deployment_id, creator_address, success
            ).transact({"from": SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"]})
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            log.info(f" transaction receipt: {tx_receipt}")
        except Exception as e:
            log.info(f"report_vnf_deletion error {e}")

    def get_vnf_details_from_contract(self, user_address):
        """
        Calls the SC function 'getVnfs' to get all vnf details for a specific user.
        :param user_address: str
        :return:
        """
        try:
            return self.contract.functions.getVnfs(user_address).call(
                {"from": SC_BACKEND_CONFIG["SC_BACKEND_ADDRESS"]}
            )
        except Exception as e:
            log.info(f"get_vnf_details_from_contract error {e}")
            return False


service = SmartContractService(contract=contract)
