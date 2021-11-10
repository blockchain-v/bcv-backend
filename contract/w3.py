from web3 import Web3
import json

url = 'http://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(url))
f = open('../bcv-contract/src/build/contracts/VNFDeployment.json')
# f = open('../bcv-frontend/src/truffle/build/contracts/VNFDeployment.json') # from frontend TODO remove
contractJSON = json.load(f)
contract = w3.eth.contract(address=contractJSON['networks']['5777']['address'], abi=contractJSON['abi'])
