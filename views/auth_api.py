import time
import json
import logging
from urllib import urlencode

import requests
from flask import Blueprint, Flask, redirect

from services.auth_services import authenticate_user, AuthServices
from services.user_services import UserServices
from services.google_auth_services import GoogleAuthServices, GoogleUserServices
from utils.helpers import construct_response_message
from status import Status

auth = Blueprint('authentication', __name__, url_prefix="/profile")


@auth.route('/signin', methods=["POST"])
@UserServices.verify_user
def login(user):
    if user:
        _session = authenticate_user(user)
        time.sleep(0.5)
        message = json.dumps(construct_response_message(message="successful login",
                                                        session=_session))

        return message, Status.HTTP_200_OK
    message = construct_response_message(message="Username Password Incorrect")
    return json.dumps(message), Status.HTTP_400_BAD_REQUEST


@auth.route('/', methods=["GET"])
@UserServices.check_user
def profile(user):
    logging.info(user)
    if user:
        message = construct_response_message(message=user)
        return json.dumps(message), Status.HTTP_200_OK
    message = construct_response_message(message="Invalid Login")
    return json.dumps(message), Status.HTTP_400_BAD_REQUEST


@auth.route('/signup', methods=["POST"])
@UserServices.verify_user_fields
def signup(request_data):
    user = AuthServices.new_user(request_data)
    message = construct_response_message(message="Account Created Successfully")
    return json.dumps(message)


@auth.route('/signout', methods=["GET"])
def logout():
    data = {"some_key": "some_value"}  # Your data in JSON-serializable type
    response = Flask.response_class(response=json.dumps(data),
                                    status=200,
                                    mimetype='application/json')
    response.headers["Access-Control-Allow-Credentials"] = True
    return response


@auth.route('/google', methods=["GET"])
def google_auth():
    url = GoogleAuthServices.google_oauth()
    return redirect(url)


@auth.route('/oauth2callback')
def callback():
    user_info = GoogleUserServices.user_details()
    session_id = AuthServices.google_oauth_authenticate_user(user_info)
    time.sleep(0.5)
    message = json.dumps(construct_response_message(message="successful login",
                                                    session=session_id))

    url = 'http://localhost:3000/session/' + session_id

    return redirect(url)

    # return redirect('http://localhost:3000/profile')

@auth.route('/oauthtokens')
def tokens():
    return 'success'
