from flask import Blueprint
from flask_login import login_required

from flask_app.models import mongo

mod = Blueprint('api', __name__)

@mod.route('/')
def hello():
    return 'Hello world!'