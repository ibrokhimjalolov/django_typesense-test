import environ

env = environ.Env()
env.read_env('.env')


TYPESENSE_CLIENT_SETTINGS = {
    'api_key': env.str('TYPESENSE_API_KEY', default='xxx'),
    'nodes': [{
        'host': env.str('TYPESENSE_HOST', default='typesense'),
        'port': env.str('TYPESENSE_PORT', default='8108'),
        'protocol': env.str('TYPESENSE_PROTOCOL', default='http'),
    }],
    'connection_timeout_seconds': 20
}


TYPESENSE_COLLECTIONS = (
    "blog.documents.PostDocument",
)
