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
    key = True
    message = "Username Password Incorrect"
    query = "/api/?key=" + str(key) + "&message=" + message
    return redirect(query)


@auth.route('/', methods=["GET"])
@UserServices.check_user
def profile(user):
    if user:
        return render_template("profile.html", name=user)
    key = request.args.get('key')
    message = request.args.get('message')
    return render_template("login.html",key=key, message=message )


@auth.route('/signin', methods=["GET"])
def account_login():
    key = True
    message = "Account Created Successfully"
    return redirect("/api/")


@auth.route('/signup', methods=["POST"])
@UserServices.verify_user_fields
def signup(request_data):
    key =  True
    message = new_user(request_data)
    return redirect("/api/")


@auth.route('/signup', methods=["GET"])
def get_signup():
    key = request.args.get('key')
    message = request.args.get('message')
    return render_template("signup.html", key=key, message=message)


@auth.route('/signout', methods=["GET"])
def logout():
    message = get_user_logged_out()
    response = redirect("/api/")
    response.set_cookie('session', '', expires=0)
    return response


@auth.route('/view', methods=["GET"])
def view_all_user():
    name = get_name()
    return name
