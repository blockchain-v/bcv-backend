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

        from eth_account.messages import defunct_hash_message
        t = w3.solidityKeccak(['address'], [user])
        address = w3.eth.account.recoverHash(t, signature=signedAddress)

        print('address', address, 'user', user)
        if user == address:
            user = User(address=user, signedAddress=signedAddress)
            user.save()
        # TODO call contract with if failed or errored
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