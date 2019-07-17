from urllib import urlencode

from flask import request
from google.appengine.api import urlfetch
import json
from config import load_config, dict_formation
from services.auth_services import AuthServices
import logging

CONFIG = load_config()


class GoogleAuthServices(object):

    @staticmethod
    def get_access_code():
        params = dict_formation(
            client_id=CONFIG.get('client_id'),
            redirect_uri=CONFIG.get('redirect_uris')[0],
            scope='email',
            access_type='offline',
            include_granted_scopes='true',
            response_type='code',
            prompt='select_account',
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
        url = GoogleAuthServices.get_access_code()
        return url

    @staticmethod
    def oauth_callback():
        tokens = GoogleAuthServices.get_tokens()
        logging.info(tokens)
        return tokens

    @staticmethod
    def get_user_info():
        tokens = GoogleAuthServices.get_tokens()
        access_token = tokens.get('access_token')
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        res = urlfetch.fetch(url, method='GET',
                             headers=headers)
        user_info = res.content
        logging.info(user_info)

        return json.loads(user_info)


class GoogleUserServices(object):

    @staticmethod
    def user_details():
        user_info = GoogleAuthServices.get_user_info()
        message = AuthServices.google_oauth_new_user(user_info)

        return user_info
