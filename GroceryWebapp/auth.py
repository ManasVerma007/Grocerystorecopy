from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from .models import User
from . import db  # Importing the db object from __init__.py
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
auth = Blueprint("auth", __name__)


# User login route

@auth.route("/user_login", methods=["GET", "POST"])
def userlogin():
    session.clear()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user with the given email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password and user.Place == "useronly":
                login_user(user)
                
                return redirect(url_for("main.userhome", userid=user.id))
            else:
                return render_template("user_login.html")
    return render_template("user_login.html")


# Admin login route

@auth.route("/admin_login", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password and user.Place == "adminonly":
                login_user(user)
                return redirect(url_for("main.adminhome", bool1=False,userid=user.id))
            else:
                return render_template("admin_login.html")
    return render_template("admin_login.html")


# User sign-up route
@auth.route("/user_signup", methods=["GET", "POST"])
def usersignup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        if (not user and len(email)>4 and len(first_name)>4 and password1==password2 and len(password1)>0 and len(password2)>0):
            new_user = User(
                email=email, first_name=first_name, password=password1, Place="useronly"
            )
            db.session.add(new_user)
            db.session.commit()
            return render_template("user_login.html")
    return render_template("user_signup.html")

@auth.route("/logout")
def logout():
    logout_user()
    session.clear()
    return render_template("base.html")
