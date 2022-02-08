from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

DB_ALIAS = 'bcv-db'
SC_ABI_PATH = os.environ.get('SC_ABI_PATH')

PORT = os.environ.get('PORT')

JWT_SECRET = os.environ.get('JWT_SECRET')

MONGODB_SETTINGS = {
    "db": DB_ALIAS,
    'host': 'localhost:27017',
    "alias": 'default',
}

TACKER_CONFIG = {
    'USERNAME': os.environ.get('TACKER_USERNAME'),
    'USER_ID': os.environ.get('TACKER_USER_ID'),
    'TENANT_NAME': os.environ.get('TACKER_TENANT_NAME'),
    'TENANT_ID': os.environ.get('TACKER_TENANT_ID'),
    'PASSWORD': os.environ.get('TACKER_PASSWORD'),
    'AUTH_URL': os.environ.get('TACKER_AUTH_URL'),
    'ENDPOINT_OVERRIDE': 'otherurl',
    'NOAUTH': 'noauth',
    'headers': {'X-Auth-Token': '',
                'User-Agent': 'python-tackerclient'},
    'BASEURL': os.environ.get('TACKER_BASEURL')
}

SC_BACKEND_CONFIG = {
    'SC_BACKEND_ADDRESS': os.environ.get('SC_BACKEND_ADDRESS'),
    'SC_BACKEND_ADDRESS_FROM': os.environ.get('SC_BACKEND_ADDRESS_FROM')
}

WEB3_CONFIG = {
    'URL': os.environ.get('W3_URL'),
}