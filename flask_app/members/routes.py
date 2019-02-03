from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import requests

import flask_app.api.routes as api

mod = Blueprint('members', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

# member content routes
@mod.route('/dashboard')
@login_required
def dashboard():
    events = api.get_events_by_user()
    return render_template('dashboard.html', events=sorted(events.json, key=lambda k: k['name']))

@mod.route('/links')
@login_required
def links():
    return render_template('links.html')

@mod.route('/contacts')
@login_required
def contacts():
   # users = Response(dumps(mongo.db.users.find({})))
    return render_template('contacts.html',)

@mod.route('/meeting_items')
@login_required
def meeting_items():
    return render_template('meeting_items.html')

@mod.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html')

@mod.route('/events')
@login_required
def events():
    events = api.events()
    return render_template('events.html', events=sorted(events.json, key=lambda k: k['name']))

@mod.route('/event/<string:event_id>')
@login_required
def event(event_id):
    event = api.get_event(event_id)
    if not event.json:
        return "Event not found."
    print(event.json['users'])
    users = api.get_user_list(event.json['users'])
    return render_template('event.html', event=event.json, event_id=str(event.json['_id']), users=list(users))

@mod.route('/create_event')
@login_required
def create_event():
    return render_template('create_event.html')