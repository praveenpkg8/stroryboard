from functools import wraps
from flask import request, redirect


from models.auth_datastore import User, Session
from services.auth_services import fetch_all_user
from services.parser import Parser
from utils.exception import UserNameAlreadyTakenException, UserNameLengthException, \
    EmailFormatException, AccountAlreadyExist, MobileNumberFormatException, \
    MobileNumberLengthException
from utils.helpers import from_datastore, parse_entity, parse_session


class UserServices:

    def __init__(self):
        pass

    @staticmethod
    def verify_user_fields(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            request_data = request.form
            required_fields = ['name', 'user_name', 'mail', 'password', 'mobile_number']
            username, mail = fetch_all_user(True)
            for key in required_fields:
                if key not in request_data:
                    pass

                if key == 'user_name':
                    try:
                        Parser.parse_unique_user_name(request_data['user_name'], username)
                    except UserNameAlreadyTakenException as e:
                        message = e.error_message
                        keys = True
                        query = "/profile/signup?key=" + str(keys) + "&message=" + message
                        return redirect(query)
                    except UserNameLengthException as e:
                        message = e.error_message
                        keys = True
                        query = "/profile/signup?key=" + str(keys) + "&message=" + message
                        return redirect(query)

                if key == 'mail':
                    try:
                        Parser.parse_email(request_data['mail'], mail)
                    except EmailFormatException as e:
                        message = e.error_message
                        keys = True
                        query = "/profile/signup?key=" + str(keys) + "&message=" + message
                        return redirect(query)
                    except AccountAlreadyExist as e:
                        message = e.error_message
                        keys = True
                        query = "/profile/signup?key=" + str(keys) + "&message=" + message
                        return redirect(query)

                if key == 'mobile_number':
                    try:
                        Parser.parse_mobile_number(request_data['mobile_number'])
                    except MobileNumberFormatException as e:
                        message = e.error_message
                        keys = True
                        query = "/profile/signup?key=" + str(keys) + "&message=" + message
                        return redirect(query)
                    except MobileNumberLengthException as e:
                        message = e.error_message
                        keys = True
                        query = "/profile/signup?key=" + str(keys) + "&message=" + message
                        return redirect(query)

            return fn(request_data)

        return decorated_function

    @staticmethod
    def verify_user(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            request_data = request.form
            user = parse_entity(from_datastore(User.user_by_username(request_data.get('user_name'))))
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
                user_details = parse_session(user)
                return fn(user_details)
            return fn(False)

        return decorated_function
