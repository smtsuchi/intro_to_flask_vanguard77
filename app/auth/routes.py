from flask import Blueprint, render_template, request, redirect, url_for

# import forms and models
from .forms import UserInfoForm
from app.models import User, Post

# create instance of blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates')

from app.models import db


@auth.route('/login')
def logMeIn():
    return render_template('login.html')

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

            return redirect(url_for('home'))


        else:
            print('Not validated! :(')
    return render_template('signup.html', form = my_form )