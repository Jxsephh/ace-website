from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config.update(
    SECRET_KEY = 'development_secret'
)

from flask_app import views

if __name__ == "__main__":
    app.run()
