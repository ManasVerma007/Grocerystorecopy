from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db  # Importing the db object from __init__.py

auth = Blueprint("auth", __name__)


# User login route
@auth.route("/user_login", methods=["GET", "POST"])
def userlogin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user with the given email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password and user.Place == "useronly":
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
                return redirect(url_for("main.adminhome", bool1=False))
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
        if user:
            flash("Email already exists.", category="error")
        elif (len(email)) < 4:
            flash("Email must be greater than 4 letters", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(password1) < 1:
            flash("Password must be at least 3 characters", category="error")
        else:
            new_user = User(
                email=email, first_name=first_name, password=password1, Place="useronly"
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            return render_template("user_login.html")
    return render_template("user_signup.html")


# # Admin sign-up route
# @auth.route("/admin_signup", methods=["GET", "POST"])
# def adminsignup():
#     if request.method == "POST":
#         email = request.form.get("email")
#         first_name = request.form.get("firstName")
#         password1 = request.form.get("password1")
#         password2 = request.form.get("password2")
#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash("Email already exists.", category="error")
#         elif (len(email)) < 1:
#             flash("Email must be greater than 4 letters", category="error")
#         elif len(first_name) < 2:
#             flash("First name must be greater than 1 character", category="error")
#         elif password1 != password2:
#             flash("Passwords do not match", category="error")
#         elif len(password1) < 1:
#             flash("Password must be at least 4 characters", category="error")
#         else:
#             new_user = User(
#                 email=email,
#                 first_name=first_name,
#                 password=password1,
#                 Place="adminonly",
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             flash("Account created!", category="success")
#             return render_template("admin_login.html")
#     return render_template("admin_signup.html")


# Logout route (Note: There's no logout logic implemented in this code)
@auth.route("/logout")
def logout():
    return render_template("signup.html")
