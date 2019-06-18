import time

from flask import Blueprint, render_template, redirect, request

from services.auth_services import new_user, authenticate_user, get_user_logged_out, get_name
from services.user_services import UserServices

auth = Blueprint('authentication', __name__, url_prefix="/profile")


@auth.route('/signin', methods=["POST"])
@UserServices.verify_user
def login(user):
    if user:
        _session = authenticate_user(user)
        response = redirect("/profile/")
        response.set_cookie("session", _session)
        time.sleep(0.5)
        return response
    key = True
    message = "Username Password Incorrect"
    query_params = "/profile/?key=" + str(key) + "&message=" + message
    return redirect(query_params)


@auth.route('/', methods=["GET"])
@UserServices.check_user
def profile(user):
    if user:
        return render_template("profile.html", data=user)
    key = request.args.get('key')
    message = request.args.get('message')
    return render_template("login.html",key=key, message=message )


@auth.route('/signin', methods=["GET"])
def account_login():
    key = True
    message = "Account Created Successfully"
    return redirect("/profile/")


@auth.route('/signup', methods=["POST"])
@UserServices.verify_user_fields
def signup(request_data):
    key =  True
    message = new_user(request_data)
    return redirect("/profile/")


@auth.route('/signup', methods=["GET"])
def get_signup():
    key = request.args.get('key')
    message = request.args.get('message')
    return render_template("signup.html", key=key, message=message)


@auth.route('/signout', methods=["GET"])
def logout():
    message = get_user_logged_out()
    response = redirect("/profile/")
    response.set_cookie('session', '', expires=0)
    return response


@auth.route('/view', methods=["GET"])
def view_all_user():
    name = get_name()
    return name
