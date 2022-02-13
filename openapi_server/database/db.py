from flask_mongoengine import MongoEngine
from mongoengine.connection import get_db
import logging

log = logging.getLogger("db")
db = MongoEngine()


def init_db(app):
    """Initializes the mongo db instance"""
    db.init_app(app)
    log.info(f"db name: {get_db().name}")
