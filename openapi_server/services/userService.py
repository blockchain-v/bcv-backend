from openapi_server.contract import contract
from openapi_server.repositories import User, Nonce, Token
from .authService import checkAuth
from .smartContractService import reportRegistrationToSC, reportUnregistrationToSC


def register(newUserAddress, signedAddress):
    """
    Registers a user in the db collection 'user'
    :param user: str, a users BC address
    :param signedAddress: str, a digital signature
    :return:
    """
    try:
        print('is register', newUserAddress, signedAddress)
        authStatus = False
        if checkAuth(claim=newUserAddress, signedClaim=signedAddress):
            print('checkauth passed')
            user = User(address=newUserAddress)
            user.save()
            authStatus = True
        else:
            print('newUserAddress != address')
        # SC callback to report status of the registration (successful/unsuccessful)
        reportRegistrationToSC(contract, newUserAddress, authStatus)
    except Exception as e:
        print(e)
        # SC callback called with success as False
        reportRegistrationToSC(contract, newUserAddress, False)


def unregister(userAddress):
    """
    Deletes a user from the db collection 'user'
    :param userAddress: str, a users BC address
    :return:
    """
    try:
        print('unregister')
        userToDelete = User.objects(address=userAddress)
        userLen = len(userToDelete)
        userToDelete.delete()
        nonceToDelete = Nonce.objects(address=userAddress)
        nonceToDelete.delete()
        tokenToDelete = Token.objects(userAddress=userAddress)
        tokenToDelete.delete()
        # SC callback to report status of the registration (successful/unsuccessful)
        # success is false if no users were found to be deleted (i.e. not yet registered)
        reportUnregistrationToSC(contract, userAddress, userLen > 0)

    except Exception as e:
        print(e)
        # SC callback called with success as False
        reportUnregistrationToSC(contract, userAddress, False)


def userRegistered(address) -> bool:
    """
    Checks if a user with the given address has been registered
    :param address:
    :return:  boolean
    """
    isRegistered = False
    try:
        User.objects.get(address=address)
        isRegistered = True
    except:
        pass
    return isRegistered
