from flask_login import UserMixin
import json

"""
User Class to keep track of Ace Members
@properties:
    first_name: denotes First name of user
    last_name : denotes Last name of user
    email : unique idenitifer
    service: denotes how many service points a user has
    flex : denotes how many flex points a user has
    fundraising : denotes how many fundrasing points a user has
    permission : denotes what kind of permission a user has
@methods:
    dump: turns User object into a json object
    load: Populates user object based on json object
"""

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.first_name = ''
        self.last_name = ''
        self.attendance = 0
        self.service = 0
        self.flex = 0
        self.fundraising = 0

def dump_user(user):
    return {'_type': 'user', 
            'id': user.id,
            'first_name': user.first_name, 
            'last_name': user.last_name,
            'attendance': user.attendance,
            'service': user.service,
            'flex': user.flex,
            'fundraising': user.fundraising}

def load_user(document):
    if document == None:
        return None
    assert document['_type'] == 'user'
    
    user = User(document['id'])
    user.first_name = document['first_name']
    user.last_name = document['last_name']
    user.attendance = document['attendance']
    user.service = document['service']
    user.flex = document['flex']
    user.fundraising = document['fundraising']
    return user