from flask import Flask, redirect, url_for, session, request, jsonify,render_template
from flask_oauthlib.client import OAuth

from flask_app import app

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

@app.route('/recruitment')
def recruitment():
    return admissions()

@app.route('/contact')
def contact():
    path, msg = get_login_info()
    return render_template('contact.html', login_path=path, login_msg=msg)
