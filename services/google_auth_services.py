import json
import uuid

from google.appengine.api import urlfetch
from urllib import urlencode

from flask import request
from config import load_config, dict_formation
from services.auth_services import AuthServices
from models.auth_datastore import Tokens

CONFIG = load_config()


class GoogleAuthServices(object):

    @staticmethod
    def get_access_code(scope, prompt, redirect='email'):
        if redirect == 'email':
            redirect_uri = CONFIG.get('redirect_uris')[0]
        elif redirect == 'contact':
            redirect_uri = CONFIG.get('redirect_uris')[2]
        params = dict_formation(
            client_id=CONFIG.get('client_id'),
            redirect_uri=redirect_uri,
            scope=scope,
            access_type='offline',
            include_granted_scopes='true',
            response_type='code',
            prompt=prompt,
        )

        return '{}?{}'.format('https://accounts.google.com/o/oauth2/v2/auth', urlencode(params))

    @staticmethod
    def get_tokens():
        code = request.args.get('code')
        params = dict_formation(
            code=code,
            client_id=CONFIG.get('client_id'),
            client_secret=CONFIG.get('client_secret'),
            redirect_uri=CONFIG.get('redirect_uris')[0],
            grant_type='authorization_code'
        )
        url = 'https://www.googleapis.com/oauth2/v4/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        res = urlfetch.fetch(url, method='POST',
                             payload=urlencode(params), headers=headers)

        tokens = res.content
        return json.loads(tokens)

    @staticmethod
    def google_oauth():
        url = GoogleAuthServices.get_access_code(scope='profile email', prompt='select_account')
        return url

    @staticmethod
    def oauth_callback():
        tokens = GoogleAuthServices.get_tokens()
        return tokens

    @staticmethod
    def get_user_info():
        tokens = GoogleAuthServices.get_tokens()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        token_id = uuid.uuid4().hex
        token_key = Tokens(
            token_id=token_id,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        res = urlfetch.fetch(url, method='GET',
                             headers=headers)
        user_info = res.content

        return json.loads(user_info), token_id


class GoogleUserServices(object):

    @staticmethod
    def user_details():
        user_info, token_id = GoogleAuthServices.get_user_info()
        message = AuthServices.google_oauth_new_user(user_info)

        return user_info, token_id
