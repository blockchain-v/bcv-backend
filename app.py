from flask import Flask
import config
from contract.w3 import contract
from database.db import init_db
from mongoengine.connection import get_db
from flask_restful import Api
from resources.routes import init_routes
from services.eventlistener import SmartContractEventListener
from services.smartContractService import registerBackend
from tacker.tacker import Tacker

# init stuff
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = config.MONGODB_SETTINGS
api = Api(app)
init_db(app)
init_routes(api)
# setup tacker connection
tacker = Tacker()
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

    # run http server
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)


if __name__ == '__main__':
    print('in main')
    main()
