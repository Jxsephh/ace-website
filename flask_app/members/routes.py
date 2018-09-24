from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
import requests

import flask_app.api.routes as api

mod = Blueprint('members', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

# member content routes
@mod.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@mod.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html')

@mod.route('/events')
@login_required
def events():
    events = api.events()
    print(events.json)
    return render_template('events.html', events=events.json)
