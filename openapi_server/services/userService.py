from openapi_server.contract import contract
from openapi_server.repositories import User, Nonce
from .authService import checkAuth
from .smartContractService import reportRegistrationToSC, reportUnregistrationToSC
import logging
from mongoengine import DoesNotExist

log = logging.getLogger('userService')


def register(newUserAddress, signedAddress):
    """
    Registers a user in the db collection 'user'
    :param newUserAddress: str, a users BC address
    :param signedAddress: str, a digital signature
    :return:
    """
    try:
        log.info(f'is register {newUserAddress}, {signedAddress}')
        authStatus = False
        if checkAuth(claim=newUserAddress, signedClaim=signedAddress):
            log.info('checkauth passed')
            user = User(address=newUserAddress)
            user.save()
            authStatus = True
        else:
            log.info('newUserAddress != address')
        # SC callback to report status of the registration (successful/unsuccessful)
        reportRegistrationToSC(contract, newUserAddress, authStatus)
    except Exception as e:
        log.info(f'register error {e}')
        # SC callback called with success as False
        reportRegistrationToSC(contract, newUserAddress, False)


def unregister(userAddress):
    """
    Deletes a user from the db collection 'user'
    :param userAddress: str, a users BC address
    :return:
    """
    try:
        log.info(f'unregister {userAddress}')
        userToDelete = User.objects(address=userAddress)
        userLen = len(userToDelete)
        userToDelete.delete()
        nonceToDelete = Nonce.objects(address=userAddress)
        nonceToDelete.delete()
        # SC callback to report status of the registration (successful/unsuccessful)
        # success is false if no users were found to be deleted (i.e. not yet registered)
        reportUnregistrationToSC(contract, userAddress, userLen > 0)

    except Exception as e:
        log.info(f'unregister error {e}')
        # SC callback called with success as False
        reportUnregistrationToSC(contract, userAddress, False)


def userRegistered(address) -> bool:
    """
    Checks if a user with the given address has been registered
    :param address:
    :return:  boolean
    """
    is_registered = False
    try:
        User.objects.get(address=address)
        is_registered = True
    except DoesNotExist:
        pass
    return is_registered
