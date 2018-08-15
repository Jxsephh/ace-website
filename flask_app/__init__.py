from flask import Flask

app = Flask(__name__, template_folder='../templates')
app.config.from_object('config')
app._static_folder = '../static'
app.secret_key = 'development'

from flask_app import routes
