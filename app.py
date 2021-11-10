from flask import Flask

import config
from contract.w3 import contract
from database.db import init_db
from mongoengine.connection import get_db

from flask_restful import Api
from resources.routes import init_routes
from services.eventlistener import start_event_listen
from services.smartContractService import registerBackend

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = config.MONGODB_SETTINGS
api = Api(app)

init_db(app)
init_routes(api)


def main():
    registerBackend(contract)
    # Blockchain Smart Contract Event Listening
    start_event_listen(contract)
    db = get_db()
    print("Database name: ", db.name)

    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)


if __name__ == '__main__':
    print('in main')
    main()
