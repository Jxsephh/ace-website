from flask_app import app
from flask import Flask, redirect, url_for, session, request, jsonify,render_template
from flask_oauthlib.client import OAuth

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

def get_login_info():
    if 'google_token' in session:
        if not 'me' in session:
            session['me'] = google.get('userinfo').data
        return 'logout', 'Log Out ' + session['me']['email']
    else:
        return 'login', 'Login'

@app.route("/")
def index():
    """
    Home page
    """
    path, msg = get_login_info()
    return render_template('index.html', login_path=path, login_msg=msg)

@app.route('/index')
def home():
    """
    redirect for home page
    """
    return index()

@app.route('/service')
def service():
    path, msg = get_login_info()
    return render_template('service.html', login_path=path, login_msg=msg)

@app.route('/officers')
def officers():
    path, msg = get_login_info()
    return render_template('officers.html', login_path=path, login_msg=msg)

@app.route('/admissions')
def admissions():
    path, msg = get_login_info()
    return render_template('admissions.html', login_path=path, login_msg=msg)

@app.route('/contact')
def contact():
    path, msg = get_login_info()
    return render_template('contact.html', login_path=path, login_msg=msg)

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

   # return jsonify({"data": me.data})
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')