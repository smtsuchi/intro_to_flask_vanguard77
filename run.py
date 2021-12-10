from app import app, db
from app.models import User, Post, Product

@app.shell_context_processor
def shell_context():
    return {'db': db, 'User':User, 'Post':Post, 'Product':Product}