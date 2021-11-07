from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
import json
from web3 import Web3
from services.eventlistener import start_event_listen

app = Flask(__name__)
api = Api(app)

url = 'http://127.0.0.1:9545'
contract_address = '0x64308228cAA0b9e96c6a05d53f54e80564358Cec'
w3 = Web3(Web3.HTTPProvider(url))

f = open('../bcv-frontend/src/truffle/build/contracts/VNFDeployment.json')
contractJSON = json.load(f)
contract = w3.eth.contract(address=contract_address, abi=contractJSON['abi'])


class User(Resource):
    def get(self):
        return {'user': ['asdf']
                }


api.add_resource(User, '/')


def main():
    # db setup. for docker can use 'mongodb://db:27017/db'
    client = MongoClient('mongodb://127.0.0.1:27017')
    database_names = client.list_database_names()
    print("\ndatabases:", database_names)

    # Blockchain Smart Contract Event Listening
    start_event_listen(contract)

    # run server
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    main()
