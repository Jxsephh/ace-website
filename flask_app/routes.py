from flask_app import app
from flask import Flask, redirect, url_for, session, request, jsonify,render_template
from flask_oauthlib.client import OAuth
import config as cfg

app.secret_key = 'development'
oauth = OAuth(app)
REDIRECT_PATH= '/oauth2callback'

google = oauth.remote_app(
    'google',
    consumer_key = app.config['GOOGLE_ID'],
    consumer_secret = app.config['GOOGLE_SECRET'],
    request_token_params = {
        'scope': 'email'
    },
    base_url = 'https://www.googleapis.com/oauth2/v1/',
    request_token_url = None,
    access_token_method = 'POST',
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
)

@app.route("/")
def index():
    """
    Home page
    """
    msg='Login'
    path_direct='login'
    if 'google_token' in session:
        me = google.get('userinfo')
        print(me.data)
        msg = 'Log Out ' +me.data['email']
        path_direct = 'logout'
    return render_template('index.html',direct=path_direct,login_msg=msg)

@app.route('/index')
def home():
    """
    redirect for home page
    """
    return index()

@app.route('/login')
def login():
    """
    Authorizes users
    """
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    """
    removes user from session
    """
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route(REDIRECT_PATH)
def authorized():
    """
    Google Authentication
    """
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
   # return jsonify({"data": me.data})
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')