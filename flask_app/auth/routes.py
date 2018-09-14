from flask import Blueprint, current_app, render_template, redirect, url_for, request, session
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_oauthlib.client import OAuth

from flask_app.models import User, mongo

mod = Blueprint('auth', __name__, template_folder='templates')

# login setup
login_manager = LoginManager()
login_manager.login_view = "login"

# google oauth setup
oauth = OAuth()
google = oauth.remote_app(
    'google',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    app_key='GOOGLE'
)

# lazy loading of things once app state is available
@mod.record_once
def on_load(state):
    login_manager.init_app(state.app)
    oauth.init_app(state.app) # loads the google secret keys from instance/config.py

@login_manager.user_loader
def get_user(user_id):
    document = mongo.db.users.find_one({'id': user_id})
    if document == None:
        user = User(user_id)
        mongo.db.users.insert_one(user.dump())
        return user
    return User.from_json(document)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@mod.route('/login')
def login():
    return google.authorize(callback=url_for('auth.oauth2callback', _external=True))

@mod.route('/oauth2callback')
def oauth2callback():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')

    if me.data.get('email') not in current_app.config.get('WHITELIST'):
        return redirect(url_for('static.index'))
    else:
        # load the user
        user = get_user(me.data.get('email'))

        # if this user didn't exist already create and save them
        if user == None:
            user = User(me.data.get('email'))
            mongo.db.users.insert_one(user.dump())

        login_user(user)
        return redirect(url_for('auth.dashboard'))

@mod.route('/logout')
@login_required
def logout():
    session.pop('google_token', None)
    logout_user()
    return redirect(url_for('static.index'))

# member content routes
@mod.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@mod.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html')
