from flask import Flask
from config import Config

# import our blueprints for registration
from .blog.routes import blog
from .auth.routes import auth
from .shop.routes import shop

from .models import db, User
# import database related
from flask_migrate import Migrate
from flask_login import LoginManager

from flask_cors import CORS

# Mail Sending stuff
# from flask_mail import Mail

app = Flask(__name__)
login = LoginManager()
CORS(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(blog)
app.register_blueprint(auth)
app.register_blueprint(shop)

app.config.from_object(Config)

# initialize our databse to work with our app
db.init_app(app)
login.init_app(app)
# mail.init_app(app)

login.login_view = 'auth.logMeIn'
login.login_message = "Tough.. Please log in to access this page."
login.login_message_category = 'danger'

migrate = Migrate(app,db)

from . import routes
from . import models
