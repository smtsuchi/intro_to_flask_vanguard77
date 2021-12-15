from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

# Create Models based off of ERD (Database Tables)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, email, password, is_admin = False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=False)
    image = db.Column(db.String(300))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, image, content, user_id):
        self.title = title 
        self.image = image
        self.content = content
        self.user_id = user_id

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=False)
    price = db.Column(db.Float())
    image = db.Column(db.String())
    description = db.Column(db.String())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, name, price, image, description):
        self.name = name
        self.price = price
        self.image = image
        self.description = description

    def to_dict(self):
        return {
            'id' : self.id,
            'name': self.name,
            'price': self.price,
            "image": self.image,
            'description': self.description,
            "created_on": self.created_on
        }

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    image = db.Column(db.String())
    ability = db.relationship('Ability', backref='pokemon', lazy=True)
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image
        
class Ability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    def __init__(self, name, pokemon_id):
        self.name = name
        self.pokemon_id = pokemon_id