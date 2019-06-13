from functools import wraps
from flask import request, session, render_template

from models.auth_datastore import User, Session
from services.auth_composed import fetch_all_user
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
                        return render_template("signup.html", key=True, message=message)
                    except UserNameLengthException as e:
                        message = e.error_message
                        return render_template("signup.html", key=True, message=message)


                if key == 'mail':
                    try:
                        Parser.parse_email(request_data['mail'], mail)
                    except EmailFormatException as e:
                        message = e.error_message
                        return render_template("signup.html", key=True, message=message)
                    except AccountAlreadyExist as e:
                        message = e.error_message
                        return render_template("signup.html", key=True, message=message)

                if key == 'mobile_number':
                    try:
                        Parser.parse_mobile_number(request_data['mobile_number'])
                    except MobileNumberFormatException as e:
                        message = e.error_message
                        return render_template("signup.html", key=True, message=message)
                    except MobileNumberLengthException as e:
                        message = e.error_message
                        return render_template("signup.html", key=True, message=message)

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
                user_details = parse_session(Session.get_session(message))
                return fn(user_details.get('name'))
            return fn(False)

        return decorated_function
