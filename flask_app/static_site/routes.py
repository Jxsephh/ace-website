from flask import Blueprint, render_template, redirect, url_for

mod = Blueprint('static', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@mod.route("/")
def home():
    return redirect(url_for('static.index'))

@mod.route('/index')
def index():
    return render_template('index.html')

@mod.route('/service')
def service():
    return render_template('service.html')

@mod.route('/officers')
def officers():
    return render_template('officers.html')

@mod.route('/admissions')
def admissions():
    return render_template('admissions.html')

@mod.route('/recruitment')
def recruitment():
    return admissions()

@mod.route('/contact')
def contact():
    return render_template('contact.html')