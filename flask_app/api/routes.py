from flask import Blueprint, request, Response
from flask_login import login_required, current_user
from http import HTTPStatus as http
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

from flask_app.api import auth_required, officer_required
from flask_app.models import mongo, Event, User

mod = Blueprint('api', __name__)

"""Just to make sure the api is returning something.
"""
@mod.route('/', methods=['GET'])
def hello():
    return Response('Hello World!', http.OK, mimetype="text/plain")

"""Get all events
"""
@mod.route('/events', methods=['GET'])
@auth_required
def events():
    return Response(dumps(mongo.db.events.find({})), http.FOUND, mimetype='application/json')

"""Get a single event
"""
@mod.route('/events/<string:event_id>', methods=['GET'])
@auth_required
def get_event(event_id):
    event = Event()
    event['_id'] = event_id

    if event.load():
        return Response(dumps(event), status=http.FOUND, mimetype="application/json")
    else:
        return Response(status=http.NOT_FOUND, mimetype="text/plain")

"""Create an event
"""
@mod.route('/events', methods=['POST'])
@auth_required
@officer_required
def create_event(): 
    args = request.form
    event = Event()
    try:
        event['name'] = args['name']
        event['creator'] = current_user._id
        event['category'] = args['category']
        event['value'] = args['value']
        event['location'] = args['location']
        event['shifts'] = args['shifts'] == 'on'
        event['info'] = args['info']
    except KeyError:
        return Response('Event did not contain all the required fields.', status=http.BAD_REQUEST, mimetype="text/plain")

    event.save()
    return Response('Successfully created event.', status=http.CREATED, mimetype="text/plain")

"""Close an event
"""
@mod.route('/events/close/<string:event_id>', methods=['GET'])
@auth_required
@officer_required
def close_event(event_id):
    event = Event()
    event['_id'] = event_id

    if not event.load():
        return Response('Event not found', status=http.NOT_FOUND, mimetype="text/plain")

    event['closed'] = True
    event.save()

    return Response('Successfully closed event.', status=http.OK, mimetype="text/plain")

"""Reopen an event
"""
@mod.route('/events/reopen/<string:event_id>', methods=['GET'])
@auth_required
@officer_required
def reopen_event(event_id):
    event = Event()
    event['_id'] = event_id

    if not event.load():
        return Response('Event not found', status=http.NOT_FOUND, mimetype="text/plain")

    event['closed'] = False
    event.save()

    return Response('Successfully closed event.', status=http.OK, mimetype="text/plain")

"""Sign up for an event
"""
@mod.route('/signup/<string:event_id>', methods=['GET'])
@auth_required
def signup(event_id):
    event = Event()
    event['_id'] = event_id

    if not event.load():
        return Response('Event not found.', status=http.NOT_FOUND)

    if not ObjectId(current_user.id) in event['users']:
        event['users'] += [ObjectId(current_user.id)]
        event.save()
    else:
        return Response('You already signed up for this event.', status=http.OK, mimetype="text/plain")

    return Response('Successfully signed up for event.', status=http.OK, mimetype="text/plain")

"""Get a user
"""
@mod.route('/users/<string:user_id>', methods=['GET'])
@auth_required
@officer_required
def get_user(user_id):
    user = User()
    user['_id'] = user_id

    if not user.load():
        return Response('User not found.', status=http.NOT_FOUND)

    return Response(dumps(user), status=http.FOUND, mimetype="application/json")