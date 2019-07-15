import uuid
import logging

from flask import session, request
from models.auth_datastore import User, Session
from utils.helpers import entity_list


class AuthServices(object):

    @staticmethod
    def new_user(request_data):
        user = User(
            name=request_data.get('name'),
            mail=request_data.get('mail'),
            password=request_data.get('password'),
        )
        res = User.create_user(user)
        return "Account Created Successfully"

    @staticmethod
    def fetch_user_by_mail(mail):
        user = User.user_by_mail(mail)
        return user

    @staticmethod
    def google_oauth_new_user(user_info):
        password = uuid.uuid4().hex
        logging.info(type(user_info))
        user = User(
            name=user_info.get('name'),
            mail=user_info.get('email'),
            password=password
        )
        res = User.create_user(user)
        return "Account Created Successfully"

    @staticmethod
    def google_oauth_authenticate_user(user):
        if user:
            session_id = str(uuid.uuid4())
            ses = Session(
                session_id=session_id,
                mail=user.get('email'),
                name=user.get('name')
            )
            res = Session.create_session(ses)
            logging.info(res)
            return session_id
        return user



def fetch_all_user():
    users = User.get_all_user()
    return entity_list(users)


def authenticate_user(user):
    if user:
        session_id = str(uuid.uuid4())
        ses = Session(
            session_id=session_id,
            mail=user.get('mail'),
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
