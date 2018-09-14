from flask import Flask, Blueprint
from flask_app.models import mongo

app = Flask(__name__, static_folder=None)
app.config.from_pyfile('config.py')

# import blueprints
from flask_app.static_site.routes import mod as static
from flask_app.member_site.routes import mod as member

# set up mongo
mongo.init_app(app)

# register blueprints
app.register_blueprint(static)
app.register_blueprint(member)

