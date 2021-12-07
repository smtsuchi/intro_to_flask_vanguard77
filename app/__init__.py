from flask import Flask

# import our blueprints for registration
from .blog.routes import blog
from .auth.routes import auth

app = Flask(__name__)

app.register_blueprint(blog)
app.register_blueprint(auth)

from app import routes