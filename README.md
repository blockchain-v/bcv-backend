# backend

# how to run this:
- until contract setup is decided we can't run this in docker yet. backend reads contract from the `bcv-contract` directory.
- dependencies are in requirements.txt, python 3.8 works (3.10 not supported)

assumed folder structure:

`blockchain-v/bcv-contract`

`blockchain-v/bcv-frontend`

`blockchain-v/bcv-backend`

`blockchain-v/bcv-docker`

1. start ganache, optionally add the `truffle-config.js` as project to read the smart contract values and see events
2. cd into `bcv-contract/src` and run `truffle migrate --reset`
3. start db: `docker compose up db`
4. in frontend change in truffleService.js: `import vnfContractData from '../../../bcv-contract/src/build/contracts/VNFDeployment.json'`
5. start frontend: `yarn serve` (we'll have to copy from the /bcv-contract at some point to run this with docker (outside of context right now))
6. start the Tacker VM
7. adjust your backend .env 
   1. to your local tacker VM config (can be read from the tacker dashboard at API Access)
   2. the SC addresses to ones from your local ganache setup (will be used to register the backend)
8. start the backend in parent directory: e.g. `python3 -m openapi_server`


# OpenAPI generated server

## Overview
This server was generated by the [OpenAPI Generator](https://openapi-generator.tech) project. By using the
[OpenAPI-Spec](https://openapis.org) from a remote server, you can easily generate a server stub.  This
is an example of building a OpenAPI-enabled Flask server.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m openapi_server
```

and open your browser to here:

```
http://localhost:8080/api/v1/bcv/ui/
```

Your OpenAPI definition lives here:

```
http://localhost:8080/api/v1/bcv/openapi.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t openapi_server .

# starting up a container
docker run -p 8080:8080 openapi_server
```