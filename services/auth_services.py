import uuid
import logging

from flask import session, request
from models.auth_datastore import User, Session
from utils.helpers import entity_list


def new_user(request_data):
    user = User(
        name=request_data.get('name'),
        user_name=request_data.get('user_name'),
        mail=request_data.get('mail'),
        password=request_data.get('password'),
        mobile_number=request_data.get('mobile_number')
    )
    res = User.create_user(user)
    return "Account Created Successfully"


def fetch_all_user(verify=False):
    users = User.get_all_user()
    return entity_list(users, verify)


def authenticate_user(user):
    if user:
        session_id = str(uuid.uuid4())
        ses = Session(
            session_id=session_id,
            user_name=user.get('user_name'),
            name=user.get('name')
        )
        res = Session.create_session(ses)
        logging.info(res)
        return session_id
    return user


def get_user_logged_out():
    if "session" in request.cookies:
        session_key = Session.get_session(request.cookies.get('session'))
        Session.delete_session(session_key)
        return "User logged out"


def get_name():
    name = session['id']
    return name
