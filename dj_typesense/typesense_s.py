import os

import environ

env = environ.Env()
env.read_env(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

TYPESENSE_CLIENT_SETTINGS = {
    'api_key': env.str('TYPESENSE_API_KEY', default='Hu52dwsas2AdxdE'),
    'nodes': [{
        'host': env.str('TYPESENSE_HOST', default='localhost'),
        'port': env.str('TYPESENSE_PORT', default='8108'),
        'protocol': env.str('TYPESENSE_PROTOCOL', default='http'),
    }],
    'connection_timeout_seconds': 20
}
