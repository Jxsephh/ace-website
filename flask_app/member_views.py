from flask import Flask, render_template, Response, redirect, url_for, request, session, abort, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_oauthlib.client import OAuth

from flask_app import app

# login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# google oauth setup
oauth = OAuth()
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# inheiriting from UserMixin provides most default implementations for this class
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        print(f"Logged in:\n{self}")

    def __repr__(self):
        return f"id:{self.id} name:{self.name} password:{self.password}"

@app.route('/members')
@login_required
def members():
    return "Members only content here."

@app.route('/login')
def login():
    return google.authorize(callback=url_for('oauth2callback', _external=True))

@app.route('/oauth2callback')
def oauth2callback():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    login_user(User(me.data.get('email')))
    return redirect(url_for('members'))

@app.route('/logout')
@login_required
def logout():
    session.pop('google_token', None)
    logout_user()
    return redirect(url_for('index'))
 
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)