import datetime
from openapi_server.database import db


class Nonce(db.Document):
    value = db.StringField(required=True, unique=True)
    address = db.StringField(required=True, unique=True)
    issueDate = db.DateTimeField(default=datetime.datetime.now)
    meta = {'collection': 'nonce'}
