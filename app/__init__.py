from flask import Flask
from config import Config

# import our blueprints for registration
from .blog.routes import blog
from .auth.routes import auth

from .models import db
# import database related
from flask_migrate import Migrate

app = Flask(__name__)

app.register_blueprint(blog)
app.register_blueprint(auth)

app.config.from_object(Config)

# initialize our databse to work with our app
db.init_app(app)

migrate = Migrate(app,db)

from . import routes
from . import models
