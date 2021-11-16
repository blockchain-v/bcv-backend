import datetime
from database import db


class Challenge(db.Document):
    address = db.StringField(required=True)
    challengeValue = db.StringField(required=True, unique=True)
    challengeDate = db.DateTimeField(default=datetime.datetime.now)
    meta = {'collection': 'challenges'}
