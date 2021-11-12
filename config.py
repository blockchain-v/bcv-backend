from dotenv import load_dotenv
import os

load_dotenv('.env')

DB_ALIAS = 'bcv-db'

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
    'ENDPOINT_URL': os.environ.get('TACKER_ENDPOINT_URL'),
    'ENDPOINT_OVERRIDE': 'otherurl',
    'NOAUTH': 'noauth',
    'headers': {'X-Auth-Token': '',
                'User-Agent': 'python-tackerclient'},
    'baseurl': os.environ.get('TACKER_BASEURL')
}
