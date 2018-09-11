from flask import Flask, render_template

from flask_app import app

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return home()

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/officers')
def officers():
    return render_template('officers.html')

@app.route('/admissions')
def admissions():
    return render_template('admissions.html')

@app.route('/recruitment')
def recruitment():
    return admissions()

@app.route('/contact')
def contact():
    return render_template('contact.html')