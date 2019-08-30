import time
import json
import logging

from flask import Blueprint, redirect, request

from services.auth_services import AuthServices
from services.user_services import UserServices
from services.google_auth_services import GoogleAuthServices, GoogleUserServices
from utils.helpers import construct_response_message
from status import Status
from config import frontend_config


from google.appengine.api import taskqueue


auth = Blueprint('authentication', __name__, url_prefix="/api/auth")


@auth.route('/signin', methods=["POST"])
@UserServices.verify_user
def login(user):
    if user:
        _session = AuthServices.authenticate_user(user)
        time.sleep(0.5)
        message = json.dumps({
            'message': "successful login",
            'session': _session
        })

        return message, Status.HTTP_200_OK
    message = construct_response_message(message="Username Password Incorrect")
    return json.dumps(message), Status.HTTP_400_BAD_REQUEST


@auth.route('/', methods=["GET"])
@UserServices.check_user
def profile(user):
    message = construct_response_message(message=user)
    return json.dumps(message), Status.HTTP_200_OK


@auth.route('/signup', methods=["POST"])
@UserServices.verify_user_fields
def signup(request_data):
    AuthServices.new_user(request_data)
    message = construct_response_message(message="Account Created Successfully")
    return json.dumps(message), Status.HTTP_201_CREATED


@auth.route('/signout', methods=["GET"])
def logout():
    message = AuthServices.get_user_logged_out()
    message = construct_response_message(message=message)
    return json.dumps(message)


@auth.route('/reset', methods=['GET'])
def reset_mail():
    url = request.args.get('mail_url')
    mail = request.args.get('mail')
    AuthServices.send_reset_link(url, mail)
    return json.dumps({'message': 'mail sent'}), Status.HTTP_200_OK


@auth.route('/reset-password', methods=['POST'])
@UserServices.check_reset_password
def update_password(request_data):
    message = AuthServices.amend_password(request_data)
    return json.dumps({'message': message}), Status.HTTP_202_ACCEPTED


@auth.route('/forgot-password', methods=['PUT'])
def reset():
    mail = request.get_json().get('mail')
    url = AuthServices.reset_password(mail)
    taskqueue.add(
        url='/api/auth/reset',
        params={
            'mail_url': url,
            'mail': mail
        },
        method='GET'
    )
    return json.dumps({'message': 'mail sent'}), Status.HTTP_200_OK


@auth.route('/google', methods=["GET"])
def google_auth():
    url = GoogleAuthServices.google_oauth()
    return redirect(url)


@auth.route('/oauth2callback')
def callback():
    user_info, token_id = GoogleUserServices.user_details()
    logging.info(user_info)
    session_id = AuthServices.google_oauth_authenticate_user(user_info, token_id)
    time.sleep(0.5)
    message = json.dumps(construct_response_message(message="successful login",
                                                    session=session_id))
    url = frontend_config().get('frontend_url') + '/sign/' + session_id + ''
    return redirect(url)


