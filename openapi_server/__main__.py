#!/usr/bin/env python3

import connexion
from flask_cors import CORS

from openapi_server.nvf_framework import tacker
from openapi_server.utils import encoder
from openapi_server import config
from openapi_server.contract import start_sc_event_listening, smartContractService
import logging

from openapi_server.services import vnfService, userService
from openapi_server.database import init_db

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)-15s] %(levelname)-8s %(message)s"
)


def main():
    app = connexion.App(__name__, specification_dir="./openapi/")
    app.app.json_encoder = encoder.JSONEncoder
    app.app.config["MONGODB_SETTINGS"] = config.MONGODB_SETTINGS
    app.add_api("openapi.yaml", arguments={"title": "BCV"}, pythonic_params=True)
    CORS(app.app)
    # connect to the db
    init_db(app.app)
    # connect to the Tacker VNF MANO Framework
    tacker.connect()
    # register the bcv-backend to the smart contract
    smartContractService.service.register_backend_in_sc()
    # start the smart contract event listening
    start_sc_event_listening(vnf_service=vnfService, user_service=userService)
    app.run(port=config.PORT, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
