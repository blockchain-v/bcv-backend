from models.user import User


def register(user, signedAddress):
    """
    Registers a user in the db
    :param user:
    :param signedAddress:
    :return:
    """
    print('is register', user, signedAddress)
    user = User(address=user, signedAddress=signedAddress)
    user.save()


def unregister():
    print('unregister')
