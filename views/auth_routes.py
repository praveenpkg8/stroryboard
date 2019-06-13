import json

from flask import Blueprint, render_template, redirect, url_for, session, request

from services.auth_composed import new_user, authenticate_user, get_user_logged_out, get_name
from services.user_composed import UserServices

auth = Blueprint('authentication', __name__, url_prefix="/api")


@auth.route('/signin', methods=["POST"])
@UserServices.verify_user
def login(user):
    if user:
        _session = authenticate_user(user)
        response = redirect("/api/")
        response.set_cookie("session", _session)
        return response
    return render_template('login.html', key=True)


@auth.route('/', methods=["GET"])
@UserServices.check_user
def profile(user):
    if user:
        return render_template("profile.html", name=user)
    return render_template("login.html", key=False)


@auth.route('/signin', methods=["GET"])
def account_login():
    message = "Account Created Suucesfully"
    return render_template('login.html', key=False, message=message, users=True)


@auth.route('/signup', methods=["POST"])
@UserServices.verify_user_fields
def signup(request_data):
    message = new_user(request_data)
    return redirect(url_for("authentication.account_login"))


@auth.route('/signup', methods=["GET"])
def get_signup():
    return render_template("signup.html")


@auth.route('/signout', methods=["GET"])
def logout():
    message = get_user_logged_out()
    response = redirect(url_for('authentication.profile'))
    response.set_cookie('session', '', expires=0)
    return response


@auth.route('/view', methods=["GET"])
def view_all_user():
    name = get_name()
    return name
