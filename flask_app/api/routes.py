from flask import Blueprint, request, Response
from flask_login import login_required, current_user
from http import HTTPStatus as http
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask_app.models import mongo, Event

mod = Blueprint('api', __name__)

@mod.route('/', methods=['GET'])
def hello():
    return Response('Hello World!', http.OK, mimetype="text/plain")

# get all events
@mod.route('/events', methods=['GET'])
def events():
    if not current_user.is_authenticated:
        print("auth failed")
        return Response('Authorization required.', status=http.UNAUTHORIZED, mimetype="text/plain")

    return Response(dumps(mongo.db.events.find({})), http.FOUND, mimetype='application/json')

# get a single event
@mod.route('/events/<string:event_id>', methods=['GET'])
def get_event(event_id):
    if not current_user.is_authenticated:
        return Response('Authorization required.', status=http.UNAUTHORIZED, mimetype="text/plain")

    # query mongodb
    db_response = mongo.db.events.find_one({'_id': ObjectId(event_id)})
    if db_response:
        return Response(dumps(db_response), status=http.FOUND, mimetype="application/json")
    else:
        return Response(status=http.NOT_FOUND, mimetype="text/plain")

# create an event
@mod.route('/events', methods=['POST'])
@login_required
def create_event():
    document = request.json
    document['_type'] = 'event'
    event = None
    try:
        event = Event.from_json(document)
        event.users = []
    except KeyError:
        return Response('Event did not contain all the required fields.', status=http.BAD_REQUEST, mimetype="text/plain")
    event.creator = current_user.id
    
    db_result = mongo.db.events.update_one(
        {'name': event.name}, 
        {'$setOnInsert': event.dump()}, 
        upsert=True
    )
    if db_result.upserted_id:
        return Response('Successfully created event.', status=http.CREATED, mimetype="text/plain")
    else:
        return Response('Event with that name already exists.', status=http.CONFLICT, mimetype="text/plain")

# close an event
@mod.route('/events/close/<string:event_id>', methods=['GET'])
def close_event(event_id):
    if not current_user.is_authenticated:
        return Response('Authorization required.', status=http.UNAUTHORIZED, mimetype="text/plain")

    db_result = mongo.db.events.update_one(
        {'_id': ObjectId(event_id), 'creator': ObjectId(current_user.id)},
        {'$set': {'closed': True}}
    )
    if db_result.matched_count:
        return Response('Successfully closed event.', status=http.OK, mimetype="text/plain")
    else:
        return Response('Event not found', status=http.NOT_FOUND, mimetype="text/plain")

# reopen an event
@mod.route('/events/reopen/<string:event_id>', methods=['GET'])
def reopen_event(event_id):
    if not current_user.is_authenticated:
        return Response('Authorization required.', status=http.UNAUTHORIZED, mimetype="text/plain")

    db_result = mongo.db.events.update_one(
        {'_id': ObjectId(event_id), 'creator': ObjectId(current_user.id)},
        {'$set': {'closed': False}}
    )
    if db_result.matched_count:
        return Response('Successfully reopened event.', status=http.OK, mimetype="text/plain")
    else:
        return Response('Event not found.', status=http.NOT_FOUND, mimetype="text/plain")

# sign up for an event
@mod.route('/signup/<string:event_id>', methods=['GET'])
def signup(event_id):
    if not current_user.id:
        return Response('Authorization required.', status=http.UNAUTHORIZED, mimetype="text/plain")

    db_result = mongo.db.events.update_one(
        {'_id': ObjectId(event_id)},
        {'$addToSet': {'users': current_user.id}}
    )
    if not db_result.matched_count:
        return Response('Event not found.', status=http.NOT_FOUND)
    elif not db_result.modified_count:
        return Response('You already signed up for this event.', status=http.OK, mimetype="text/plain")
    else:
        return Response('Successfully signed up for event.', status=http.OK, mimetype="text/plain")

#@mod.route('/remove_user/<string:user_id>/')
