import datetime
from database import db


class User(db.Document):
    address = db.StringField(required=True, unique=True)
    registered_date = db.DateTimeField(default=datetime.datetime.now)
    meta = { 'collection': 'users'}
