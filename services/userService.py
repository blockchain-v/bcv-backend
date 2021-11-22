from contract import w3, contract
from models.user import User
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
        if checkAuth(newUserAddress, signedAddress):
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


def unregister(newUserAddress):
    """
    Deletes a user from the db collection 'user'
    :param user: str, a users BBC address
    :return:
    """
    try:
        print('unregister')
        userToDelete = User.objects(address=newUserAddress)
        userToDelete.delete()
        # SC callback to report status of the registration (successful/unsuccessful)
        # success is false if no users were found to be deleted (i.e. not yet registered)
        reportRegistrationToSC(contract, newUserAddress, len(userToDelete) > 0)

    except Exception as e:
        print(e)
        # SC callback called with success as False
        reportUnregistrationToSC(contract, newUserAddress, False)
