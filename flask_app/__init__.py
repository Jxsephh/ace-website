from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config.from_pyfile('config.py')

from flask_app import views
from flask_app import member_views

if __name__ == "__main__":
    app.run()
