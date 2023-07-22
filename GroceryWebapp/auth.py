from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint("auth", __name__)


@auth.route('/user_login', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        print(email, password)
        if user:
            if (user.password == password and user.Place == "useronly"):
                print("ha")
                flash('Logged in successfully!', category='success')
                return redirect(url_for('main.userhome'))
            else:
                flash('Incorrect password, try again.', category='error')
                return render_template("user_login.html")
        else:
            flash('Email does not exist.', category='error')
    return render_template("user_login.html")


@auth.route('/admin_login',methods=['GET', 'POST'])
def adminlogin():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        print(email, password)
        if user:
            if (user.password == password and user.Place == "adminonly"):
                print("hi")
                flash('Logged in successfully!', category='success')
                # user gets remembered and dont have to login every single time you visit website.
                login_user(user, remember=True)
                return redirect(url_for('main.adminhome',bool1=False))
            else:
                flash('Incorrect password, try again.', category='error')
                return render_template("admin_login.html")
        else:
            flash('Email does not exist.', category='error')
    return render_template("admin_login.html", user=current_user)



@auth.route('/user_signup', methods=['GET', 'POST'])
def usersignup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif (len(email)) < 4:
            flash('email must be > than 4 letters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 1:
            flash('password must be at least 3 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=password1, Place="useronly")
# defined all the fields in models.py of 'User' and set them = to the variables here.(line 33,34)

            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return render_template("user_login.html")
    return render_template("user_signup.html", user=current_user)


@auth.route('/admin_signup', methods=['GET', 'POST'])
def adminsignup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif (len(email)) < 1:
            flash('email must be > than 4 letters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 1:
            flash('password must be at least 4 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=password1,Place="adminonly" )
# defined all the fields in models.py of 'User' and set them = to the variables here.(line 33,34)

            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return render_template("home_admin.html")  
    return render_template("admin_signup.html")


@auth.route('/logout')
def logout():
    return render_template("signup.html")
