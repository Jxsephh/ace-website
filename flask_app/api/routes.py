from flask import Blueprint, request, Response
from flask_login import login_required, current_user
from http import HTTPStatus as http
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

from flask_app.api import auth_required, officer_required
from flask_app.models import mongo, NewEvent, User

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
    # query mongodb
    db_response = mongo.db.events.find_one({'_id': ObjectId(event_id)})
    if db_response:
        return Response(dumps(db_response), status=http.FOUND, mimetype="application/json")
    else:
        return Response(status=http.NOT_FOUND, mimetype="text/plain")

"""Create an event
"""
@mod.route('/events', methods=['POST'])
@auth_required
@officer_required
def create_event(): 
    args = request.form
    print(request.form)
    event = None
    try:
        event = NewEvent.new_event(
            args['name'],
            current_user._id,
            args['category'],
            args['value'],
            args['location'],
            args['info']
        )
    except KeyError:
        return Response('Event did not contain all the required fields.', status=http.BAD_REQUEST, mimetype="text/plain")
    
    db_result = mongo.db.events.update_one(
        {'name': event.name}, 
        {'$setOnInsert': event}, 
        upsert=True
    )
    if db_result.upserted_id:
        return Response('Successfully created event.', status=http.CREATED, mimetype="text/plain")
    else:
        return Response('Event with that name already exists.', status=http.CONFLICT, mimetype="text/plain")

"""Close an event
"""
@mod.route('/events/close/<string:event_id>', methods=['GET'])
@auth_required
@officer_required
def close_event(event_id):
    db_result = mongo.db.events.update_one(
        {'_id': ObjectId(event_id), 'creator': ObjectId(current_user.id)},
        {'$set': {'closed': True}}
    )
    if db_result.matched_count:
        return Response('Successfully closed event.', status=http.OK, mimetype="text/plain")
    else:
        return Response('Event not found', status=http.NOT_FOUND, mimetype="text/plain")

"""Reopen an event
"""
@mod.route('/events/reopen/<string:event_id>', methods=['GET'])
@auth_required
@officer_required
def reopen_event(event_id):
    db_result = mongo.db.events.update_one(
        {'_id': ObjectId(event_id), 'creator': ObjectId(current_user.id)},
        {'$set': {'closed': False}}
    )
    if db_result.matched_count:
        return Response('Successfully reopened event.', status=http.OK, mimetype="text/plain")
    else:
        return Response('Event not found.', status=http.NOT_FOUND, mimetype="text/plain")

"""Sign up for an event
"""
@mod.route('/signup/<string:event_id>', methods=['GET'])
@auth_required
def signup(event_id):
    # add user to event's users list if they are not already there
    db_result = mongo.db.events.update_one(
        {'_id': ObjectId(event_id)},
        {'$addToSet': {'users': current_user.id}}
    )
    if not db_result.matched_count:
        return Response('Event not found.', status=http.NOT_FOUND)
    elif not db_result.modified_count:
        return Response('You already signed up for this event.', status=http.OK, mimetype="text/plain")

    # get the event information
    db_result = mongo.db.events.find_one({'_id': ObjectId(event_id)})
    event = NewEvent(db_result)

    # update user's point category
    db_result = mongo.db.users.update_one(
        {'_id': ObjectId(current_user.id)},
        {'$inc': {event.category: event.value}}
    )

    if db_result.modified_count:
        return Response('Successfully signed up for event.', status=http.OK, mimetype="text/plain")
    else:
        return Response('Error. Data in the database is inconsistent.', status=http.INTERNAL_SERVER_ERROR, mimetype="text/plain")

"""Get a user
"""
@mod.route('/users/<string:user_id>')
@auth_required
@officer_required
def get_user(user_id):
    db_response = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if db_response:
        return Response(dumps(db_response), status=http.FOUND, mimetype="application/json")
    else:
        return Response(status=http.NOT_FOUND, mimetype="text/plain")