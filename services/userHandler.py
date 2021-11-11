from models.user import User


def register(user, signedAddress):
    """
    Registers a user in the db collection 'user'
    :param user: str, a users BC address
    :param signedAddress: str, a digital signature
    :return:
    """
    print('is register', user, signedAddress)
    user = User(address=user, signedAddress=signedAddress)
    user.save()


def unregister(user):
    """
    Deletes a user from the db collection 'user'
    :param user: str, a users BBC address
    :return:
    """
    print('unregister')
    userToDelete = User.objects(address=user)
    userToDelete.delete()
