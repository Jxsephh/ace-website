from flask import Flask, render_template, redirect, url_for, request, session, jsonify, g
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_oauthlib.client import OAuth
from flask_app.user import User, load_user, dump_user
from flask_pymongo import PyMongo

from flask_app import app

# database setup
mongo = PyMongo(app)
db_users = mongo.db.users

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

    if me.data.get('email') not in app.config.get('WHITELIST'):
        return redirect(url_for('index'))
    else:
        # load the user
        user = get_user(me.data.get('email'))

        # if this user didn't exist already create and save them
        if user == None:
            user = User(me.data.get('email'))
            db_users.insert_one(dump_user(user))

        login_user(user)
        return redirect(url_for('dashboard'))

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
def get_user(user_id):
    return load_user(db_users.find_one({'id': user_id}))

# member content routes
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html')
