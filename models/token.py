import datetime
from database import db


class Token(db.Document):
    value = db.StringField(required=True, unique=True)
    issueDate = db.DateTimeField(default=datetime.datetime.now)
    userAddress = db.StringField(required=True, unique=True)
    meta = {'collection': 'tokens'}
