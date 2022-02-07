from web3 import Web3
import json
import config

url = config.WEB3_CONFIG['URL']
w3 = Web3(Web3.HTTPProvider(url))

with open(config.SC_ABI_PATH) as f:
    contractJSON = json.load(f)

contract = w3.eth.contract(address=contractJSON['networks']['5777']['address'], abi=contractJSON['abi'])
