import logging
from web3 import Web3
import json
import os
from openapi_server import config

url = config.WEB3_CONFIG["URL"]
w3 = Web3(Web3.HTTPProvider(url))

directory_path = os.getcwd()
sc_path = os.path.abspath(config.SC_ABI_PATH)

if os.path.isfile(sc_path):
    pass
elif os.path.isfile(os.path.join(directory_path, "../" + config.SC_ABI_PATH)):
    # sphinx
    sc_path = os.path.join(directory_path, "../" + config.SC_ABI_PATH)
else:
    logging.error("contract not found")

with open(sc_path) as f:
    contractJSON = json.load(f)
contract = w3.eth.contract(
    address=contractJSON["networks"]["5777"]["address"], abi=contractJSON["abi"]
)
