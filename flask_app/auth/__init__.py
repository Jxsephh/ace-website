from flask import Response
from http import HTTPStatus as http
from functools import wraps
from flask_login import current_user
from flask_app.models import mongo
from bson.objectid import ObjectId

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return Response('Authorization required.', status=http.UNAUTHORIZED, mimetype="text/plain")
        return f(*args, **kwargs)
    return decorated_function

def officer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_officer:
            return Response('Only officers can perform this action.', status=http.UNAUTHORIZED, mimetype="text/plain")
        return f(*args, **kwargs)
    return decorated_function