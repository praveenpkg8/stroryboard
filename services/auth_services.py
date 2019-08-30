import logging
import uuid

from flask import request
from models.auth_datastore import User, Session, ResetPassword

from google.appengine.api import mail
from config import frontend_config


class AuthServices(object):

    @staticmethod
    def new_user(request_data):
        message = User.create_user(
            name=request_data.get('name'),
            mail=request_data.get('mail'),
            password=request_data.get('password'),
        )
        return message

    @staticmethod
    def check_for_user(mail):
        user = User.user_by_mail(mail)
        return user

    @staticmethod
    def google_oauth_new_user(user_info):

        password = uuid.uuid4().hex
        user = AuthServices.check_for_user(user_info.get('email'))

        if user is None:
            message = User.create_user(
                name=user_info.get('name'),
                mail=user_info.get('email'),
                password=password,
            )
            return message

    @staticmethod
    def google_oauth_authenticate_user(user, token_id):

        if user:

            session_id = str(uuid.uuid4())
            ses = Session(
                session_id=session_id,
                mail=user.get('email'),
                name=user.get('name'),
                token_id=token_id
            )
            Session.create_session(ses)

            return session_id

        return user

    @staticmethod
    def authenticate_user(user):

        if user:

            session_id = str(uuid.uuid4())
            ses = Session(
                session_id=session_id,
                mail=user.get('mail'),
                name=user.get('name')
            )
            Session.create_session(ses)

            return session_id

        return user

    @staticmethod
    def get_user_logged_out():

        if "session" in request.cookies:

            session_key = Session.get_session(request.cookies.get('session'))
            Session.delete_session(session_key)
            return "User logged out"

    @staticmethod
    def amend_password(request_data):
        reset_id = request_data.get('slug')
        password = request_data.get('password')
        mail = ResetPassword.get_mail(reset_id)
        if mail:
            User.change_password(mail, password)
            return "Password reset successfully"

    @staticmethod
    def reset_password(mail):
        user = User.user_by_mail(mail)
        if user is None:
            return
        frontend_url = frontend_config().get('frontend_url')
        slug = uuid.uuid4().hex
        url = '{0}/reset-password/{1}'.format(frontend_url, slug)
        ResetPassword.create_reset(slug, mail)
        return url

    @staticmethod
    def send_reset_link(url, email):
        sender_address = 'admin@full-services.appspotmail.com'
        message = mail.EmailMessage(
            sender=sender_address,
            subject="Your account has been approved")
        message.to = email
        message.body = """Dear User:

                    There have been a password reset request sent for your
                    account in order to reset your link click the below link
                    {}
                    """.format(url)
        message.send()
