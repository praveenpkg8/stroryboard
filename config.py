import os
import json

DATA_BACKEND = 'datastore'
PROJECT_ID = 'full-services'

environment = 'production'


def dict_formation(**kwargs):
    return kwargs


def load_config(application='web'):
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'client_secret.json')
    client_secret = json.load(open('client_secret.json'))
    redirect_uris = client_secret.get(application).get('redirect_uris')
    redirect_uri = redirect_uris

    if environment == 'production':
        redirect_uri = redirect_uris[3:6]

    config = dict_formation(
        redirect_uris=redirect_uri,
        token_uri=client_secret.get(application).get('token_uri'),
        auth_provider_x509_cert_url=client_secret.get(application).get('auth_provider_x509_cert_url'),
        auth_uri=client_secret.get(application).get('auth_uri'),
        client_id=client_secret.get(application).get('client_id'),
        client_secret=client_secret.get(application).get('client_secret'),
        project_id=client_secret.get(application).get('project_id'),
        javascript_origins=client_secret.get(application).get('javascript_origins')
    )
    return config


def frontend_config(environment=environment):
    if environment == 'development':
        config = dict_formation(
            frontend_url='http://localhost:3000'
        )
        return config

    elif environment == 'production':
        config = dict_formation(
            frontend_url='https://full-services.appspot.com'
        )
        return config
