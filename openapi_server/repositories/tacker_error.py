from openapi_server.database import db


class TackerError(db.Document):
    """
    Used to store tacker deployment errors into the db, so that clients can query for the errors.
    As such, no private informations are leaked through the smart contract
    """

    address = db.StringField(required=True, unique=False)
    deployment_id = db.IntField(required=False, unique=True)
    vnf_id = db.StringField(required=False, unique=False)
    type = db.StringField(required=False, unique=False)
    message = db.StringField(required=False, unique=False)
    detail = db.StringField(required=False, unique=False)
    meta = {"collection": "tacker_error"}
