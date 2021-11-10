import datetime
from database.db import db


class User(db.Document):
    address = db.StringField(required=True, unique=True)
    signedAddress = db.StringField(required=True)
    registered_date = db.DateTimeField(default=datetime.datetime.now)
    meta = { 'collection': 'users'}
