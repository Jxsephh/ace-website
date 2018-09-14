from flask import Flask, Blueprint
from flask_app import config
from flask_app.models import mongo

app = Flask(__name__, static_folder=None, instance_relative_config=True)
app.config.from_object(config)
app.config.from_pyfile('config.py')

# import blueprints
from flask_app.static_site.routes import mod as static
from flask_app.auth.routes import mod as auth
from flask_app.members.routes import mod as members
from flask_app.api.routes import mod as api

# set up mongo
mongo.init_app(app)

# register blueprints
app.register_blueprint(static)
app.register_blueprint(auth)
app.register_blueprint(members, url_prefix='/members')
app.register_blueprint(api, url_prefix='/api')

