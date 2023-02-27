from django.conf import settings
from typesense import Client


def get_typesense_client() -> Client:
    return Client(settings.TYPESENSE_CLIENT_SETTINGS)
