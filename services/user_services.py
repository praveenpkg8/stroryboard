import json
import logging

from functools import wraps
from flask import request

from models.auth_datastore import User, Session
from services.auth_services import AuthServices

from services.parser import Parser
from utils.exception import EmailFormatException, AccountAlreadyExist
from utils.helpers import from_datastore, parse_entity, parse_session, construct_response_message


class UserServices:

    def __init__(self):
        pass

    @staticmethod
    def verify_user_fields(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            request_data = request.get_json()
            required_fields = ['name', 'mail', 'password']
            mail_taken = AuthServices.fetch_user_by_mail(request_data.get('mail'))
            for key in required_fields:
                if key not in request_data:
                    pass
                if key == 'mail':
                    try:
                        Parser.parse_email(request_data.get('mail'), mail_taken)
                    except EmailFormatException as e:
                        message = construct_response_message(message=e.error_message)
                        return json.dumps(message)
                    except AccountAlreadyExist as e:
                        message = construct_response_message(message=e.error_message)
                        return json.dumps(message)

            return fn(request_data)

        return decorated_function

    @staticmethod
    def verify_user(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            request_data = request.get_json()
            user = parse_entity(from_datastore(User.user_by_mail(request_data.get('mail'))))
            if user is None:
                return fn(False)
            if user.get('password') != request_data.get('password'):
                return fn(False)
            return fn(user)

        return decorated_function

    @staticmethod
    def check_user(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if 'session' in request.cookies:
                message = request.cookies.get('session')
                user = Session.get_session(message)
                if user is not None:
                    user_details = parse_session(user)
                    return fn(user_details)
            return fn(False)

        return decorated_function
