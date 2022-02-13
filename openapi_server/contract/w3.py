from web3 import Web3
import json
import os
from openapi_server import config
from pathlib import Path

url = config.WEB3_CONFIG["URL"]
w3 = Web3(Web3.HTTPProvider(url))

directory_path = os.getcwd()

p = Path(__file__).with_name("VNFDeployment.json")
with p.open("r") as f:
    contractJSON = json.load(f)


contract = w3.eth.contract(
    address=config.WEB3_CONFIG["W3_CONTRACT_ADDRESS"], abi=contractJSON["abi"]
)
