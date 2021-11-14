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
        # TODO check what we actually do with the signature
        # s = w3.eth.account.recoverHash(signedAddress, signature=user)
        # print('s: ', s)
        user = User(address=user, signedAddress=signedAddress)
        user.save()
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
    except Exception as e:
        print(e)