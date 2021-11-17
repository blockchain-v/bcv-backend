from contract import w3, contract
from models.user import User
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
        # use same hashfunction as in contract to hash the userAddress
        t = w3.solidityKeccak(['address'], [newUserAddress])
        # using the signature, recover the address from the hash
        # this is done to check whether the digital signature was issued by the userAddress
        # if this matches, save the user to the db
        address = w3.eth.account.recoverHash(t, signature=signedAddress)
        print('address', address, 'user', newUserAddress)

        if newUserAddress == address:
            user = User(address=newUserAddress)
            user.save()
        else:
            print('newUserAddress != address', newUserAddress, address)
        # SC callback to report status of the registration (successful/unsuccessful)
        reportRegistrationToSC(contract, newUserAddress, newUserAddress == address)
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
