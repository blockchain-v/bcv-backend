import datetime
from database import db


class Token(db.Document):
    address = db.StringField(required=True)
    value = db.StringField(required=True, unique=True)
    issueDate = db.DateTimeField(default=datetime.datetime.now)
    meta = {'collection': 'tokens'}
