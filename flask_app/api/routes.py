from flask import Blueprint, request, Response
from flask_login import login_required, current_user
from http import HTTPStatus as http
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

from flask_app.auth import auth_required, officer_required
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

"""Get all events a user has signed up for
"""
@mod.route('/eventsbyuser')
@auth_required
def get_events_by_user():
    return Response(dumps(mongo.db.events.find({'users': ObjectId(current_user['_id'])})),
        status=http.FOUND, mimetype="application/json")

"""Create an event
"""
@mod.route('/events', methods=['POST'])
@auth_required
@officer_required
def create_event(): 
    args = request.form
    event = Event()
    event.update({
        'name': args['name'],
        'creator': current_user._id,
        'category': args['category'],
        'value': args['value'],
        'location': args['location'],
        'shifts': 'shifts' in args,
        'info': args['info']
    })
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
    if not str(current_user._id) == str(event['creator']):
        return Response('You can only close events you created.', status=http.OK, mimetype="text/plain")

    event['closed'] = True
    event.save()

    return Response('Closed event.', status=http.OK, mimetype="text/plain")

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
    if not str(current_user._id) == str(event['creator']):
        return Response('You can only open events you created.', status=http.OK, mimetype="text/plain")

    event['closed'] = False
    event.save()

    return Response('Reopened event.', status=http.OK, mimetype="text/plain")

"""Sign up for an event
"""
@mod.route('/signup/<string:event_id>', methods=['GET'])
@auth_required
def signup(event_id):
    event = Event()
    event['_id'] = event_id

    if not event.load():
        return Response('Event not found.', status=http.NOT_FOUND)

    if event['closed']:
        return Response('Event has closed.', status=http.OK)

    if not ObjectId(current_user._id) in event['users']:
        event['users'] += [ObjectId(current_user.id)]
        mongo.db.events.update_one( # not error checking because this should never fail
            {'_id': event['_id']},
            {'$push': {'users': ObjectId(current_user._id)}}
        )
    else:
        return Response('You already signed up for this event.', status=http.OK, mimetype="text/plain")

    return Response('Successfully signed up for event.', status=http.OK, mimetype="text/plain")

"""Get a user
"""
@mod.route('/users/<string:user_id>', methods=['GET'])
@auth_required
def get_user(user_id):
    user = User()
    user['_id'] = user_id

    if not user.load():
        return Response('User not found.', status=http.NOT_FOUND)

    return Response(dumps(user), status=http.FOUND, mimetype="application/json")

"""Gets a list of users by ObjectIds
Used to display the list of users who signed up for an event.
"""
@mod.route('/users', methods=['POST'])
def get_user_list_route(): # this route is broken atm
    ids = request.get_json()
    return Response(dumps(get_user_list(ids)), status=http.FOUND, mimetype="application/json")
def get_user_list(ids):
    print(ids)
    users = mongo.db.users.find({'_id': {'$in': [ObjectId(i['$oid']) for i in ids]}})
    return list(users)

"""Search for a single user
"""
@mod.route('/users', methods=['GET'])
@auth_required
@officer_required
def search_user():
    key = request.args.get('key')
    val = request.args.get('val')

    if not key and val:
        return Response('Query string requires "key" and "val" arguments.', status=http.BAD_REQUEST)

    user = User()
    user[key] = val

    if not user.load(key):
        return Response('User not found.', status=http.NOT_FOUND)

    return Response(dumps(user), status=http.FOUND, mimetype="application/json")

@mod.route('/promote_user', methods=['GET'])
@auth_required
@officer_required
def promote_user():
    key = request.args.get('key')
    val = request.args.get('val')

    if not key and val:
        return Response('Query string requires "key" and "val" arguments.', status=http.BAD_REQUEST)

    user = User()
    user[key] = val

    if not user.load(key):
        return Response('User not found.', status=http.NOT_FOUND)
    
    user['is_officer'] = True
    user.save()

    return Response('Promoted user.', status=http.OK)