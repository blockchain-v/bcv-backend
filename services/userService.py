from contract.w3 import w3
from models.user import User


def register(user, signedAddress):
    """
    Registers a user in the db collection 'user'
    :param user: str, a users BC address
    :param signedAddress: str, a digital signature
    :return:
    """
    try:
        print('is register', user, signedAddress)

        t = w3.solidityKeccak(['address'], [user])
        address = w3.eth.account.recoverHash(t, signature=signedAddress)

        print('address', address, 'user', user)
        # TODO call contract with if failed or errored
        if user == address:
            user = User(address=user)
            user.save()
        else:
            print('user != address', user, address)
    except Exception as e:
        print(e)


def unregister(user):
    """
    Deletes a user from the db collection 'user'
    :param user: str, a users BBC address
    :return:
    """
    try:
        print('unregister')
        userToDelete = User.objects(address=user)
        userToDelete.delete()
        # TODO call contract with if failed or errored

    except Exception as e:
        print(e)
