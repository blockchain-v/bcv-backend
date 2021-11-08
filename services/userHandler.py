from globals.db import db

def register(user, signedAddress):
    """
    Registers a user in the db
    :param user:
    :param signedAddress:
    :return:
    """
    print('is register', user, signedAddress )
    db.collection['users'].insert_one({'address':user, 'signedAddress':signedAddress})
    print(list(db.collection['users'].find({})))

def unregister():
    print('unregister')