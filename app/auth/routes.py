from flask import Blueprint, json, render_template, request, redirect, url_for, flash, get_flashed_messages, jsonify
from werkzeug.security import check_password_hash

# import forms and models
from .forms import LoginForm, UserInfoForm
from app.models import User, Post

# import login stuff
from flask_login import login_user, logout_user

# import mail messaging stuff
# from flask_mail import Message, Mail

# create instance of blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates')

# mail = Mail()

from app.models import db


@auth.route('/login', methods=['GET',"POST"])
def logMeIn():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        # check if user exists
        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect username or password.', 'danger')
            return redirect(url_for('auth.logMeIn'))
        
        # log me in
        login_user(user, remember = remember_me)
        flash('You have successfully signed in', 'success')

        return redirect(url_for('home'))

    return render_template('login.html', form = form)

@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    my_form = UserInfoForm()
    if request.method == "POST":
        if my_form.validate():
            
            username = my_form.username.data
            email = my_form.email.data
            password = my_form.password.data

            # create instance new user
            user = User(username, email, password)
            # add instance to databse
            db.session.add(user)
            # commit to databse
            db.session.commit()

            # msg = Message(
            #     f"Welcome to Shoha's Bike Shop, {username}",
            #     body="Thank you for joining our mailing list. We sell only the best bikes. Here's a coupon :]",
            #     recipients=[email]
            # )

            # mail.send(msg)
            

            flash(f'You have successfully created a new user.. Welcome, {username}', 'success')
            return redirect(url_for('home'))


        else:
            flash(f'Unsuccessful attempt. Please double check and submit the form again', 'danger')
            redirect(url_for('auth.signMeUp'))
    return render_template('signup.html', form = my_form )

@auth.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('auth.logMeIn'))


@auth.route('/api/login', methods=["POST"])
def apiLogin():
    data = request.json
    print(data)

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({
            'status': 'error',
            'message': "Incorrect username or password"
        })
    return jsonify({
        'status': 'success',
        'message': f"Welcome back, {username}",
        "data": user.to_dict(),
        "token": user.apitoken

    })

@auth.route('/api/register', methods=["POST"])
def apiRegister():
    data = request.json
    print(data)

    username = data['username']
    email = data['email']
    password = data['password']
    confirm_pass = data['confirmPassword']

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
            'status': 'error',
            'message': "User with that username already exists"
        })
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            'status': 'error',
            'message': "User with that email already exists"
        })

    if password == confirm_pass:
        u = User(username, email, password)

        db.session.add(u)
        db.session.commit()
        return jsonify(
            {
                'status': 'success',
                'data': u.to_dict(),
                'message': f"Account successfully created for {username}"
            }
        )
    
    return {'status': 'error', "message": "Passwords do not match"} 