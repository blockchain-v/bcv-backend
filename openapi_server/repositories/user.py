import datetime
from openapi_server.database import db


class User(db.Document):
    """
    Registered Users, from the smart contract
    """

    address = db.StringField(required=True, unique=True)
    registered_date = db.DateTimeField(default=datetime.datetime.now)
    meta = {"collection": "user"}
