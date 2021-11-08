from flask import Flask
from flask_restful import Resource, Api
import json
from services.eventlistener import start_event_listen
from services.smartContractService import registerBackend
from globals.db import client
from globals.w3 import w3, contract_address
app = Flask(__name__)
api = Api(app)


f = open('../bcv-contract/src/build/contracts/VNFDeployment.json')
contractJSON = json.load(f)
contract = w3.eth.contract(address=contract_address, abi=contractJSON['abi'])


class User(Resource):
    def get(self):
        return {'user': ['asdf']
                }


api.add_resource(User, '/')


def main():
    database_names = client.list_database_names()
    print("\ndatabases:", database_names)

    registerBackend(contract)
    # Blockchain Smart Contract Event Listening
    start_event_listen(contract)

    # run server
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    main()
