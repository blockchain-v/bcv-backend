#!/usr/bin/env python3

import connexion
from flask_cors import CORS
from openapi_server.utils import encoder
from openapi_server import config
from openapi_server.contract import start_sc_event_listening
import logging

from openapi_server.services import smartContractService, vnfService, userService
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
    init_db(app.app)
    smartContractService.service.register_backend_in_sc()
    start_sc_event_listening(vnf_service=vnfService, user_service=userService)
    app.run(port=8080, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
