from functools import wraps
from flask import request, jsonify

from app.models import User

# here we are creating the @token_required decorator for protecting out API routes

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Missing auth token. Please log in to a user that has a token'
            })
        u = User.query.filter_by(apitoken=token).first()
        if not u:
            return jsonify({
                'status': 'error',
                'message': 'That token does not belong to a valid user'
            })
        return func(*args, **kwargs)
    return decorated