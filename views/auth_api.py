import time
import json
import logging

from flask import Blueprint, render_template, redirect, request

from services.auth_services import new_user, authenticate_user, get_user_logged_out, get_name
from services.user_services import UserServices
from utils.helpers import construct_response_message
from status import Status

auth = Blueprint('authentication', __name__, url_prefix="/profile")


@auth.route('/signin', methods=["POST"])
@UserServices.verify_user
def login(user):
    if user:
        _session = authenticate_user(user)
        time.sleep(0.5)
        message = construct_response_message(message="successful login",
                                             session=_session)
        return json.dumps(message), Status.HTTP_200_OK
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
    message = construct_response_message(message="Account Created Successfully")
    return json.dumps(message)


@auth.route('/signout', methods=["GET"])
def logout():
    response = redirect("/profile/")
    response.set_cookie('session', '', expires=0)
    message = construct_response_message(message="Logged Out Successfully")
    return json.dumps(message)
