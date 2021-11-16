from flask import Flask
from flask_restful import Api

import config
from contract import contract
from database import init_db
from mongoengine.connection import get_db
from resources import init_routes
from services import SmartContractEventListener, registerBackend
from tacker import tacker

# init stuff
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = config.MONGODB_SETTINGS
api = Api(app)

init_db(app)
init_routes(api)

# Blockchain Smart Contract Event Listening
eventListener = SmartContractEventListener(contract, tacker)


def main():
    # register backend in the smart contract
    registerBackend(contract)

    # todo just for debugging purposes, remove this
    db = get_db()
    print("Database name: ", db.name)
    tacker.get_vims()
    tacker.get_vnfs()
    tacker.get_vnfds()

    # run http server
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)


if __name__ == '__main__':
    print('in main')
    main()
