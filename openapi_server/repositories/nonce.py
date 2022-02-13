import datetime
from openapi_server.database import db


class Nonce(db.Document):
    """
    Used to issue tokens
    Nonces get deleted when
    - a token is issued
    - a new nonce is requested
    They are 1d valid.
    """

    value = db.StringField(required=True, unique=True)
    address = db.StringField(required=True, unique=True)
    issueDate = db.DateTimeField(default=datetime.datetime.now)
    meta = {"collection": "nonce"}
