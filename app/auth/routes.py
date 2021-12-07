from flask import Blueprint
from flask import render_template

# create instance of blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/login')
def logMeIn():
    return render_template('login.html')

@auth.route('/signup')
def signMeUp():
    return render_template('signup.html')