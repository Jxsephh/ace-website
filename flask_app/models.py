from flask import jsonify, Response
from flask_login import UserMixin
from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId

# only here so this can be imported in multiple blueprints after being instantiated once
# in __init__.py
mongo = PyMongo()

class Model(dict):
    """
    A simple model that wraps mongodb document
    """
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self):
        if self._id == None:
            self._id = str(self.collection.insert(self))
        else:
            self.collection.update(
                { "_id": ObjectId(self._id) }, self)

    def reload(self):
        if self._id != None:
            self.update(self.collection.find_one({"_id": ObjectId(self._id)}))
        elif self.email != None:
            self.update(self.collection.find_one({"email": self.email}))

    def remove(self):
        if self._id != None:
            self.collection.remove({"_id": ObjectId(self._id)})
            self.clear()

    def is_loaded(self):
        return self._id != None

class NewUser(UserMixin, Model):
    collection = MongoClient()['data']['users']

    @property
    def id(self):
        return self._id

class User(UserMixin):
    MEMBER = 2
    OFFICER = 1
    ADMIN = 0

    # users always have at least an email
    def __init__(self, email):
        self.id = None
        self.email = email
        self.first_name = ''
        self.last_name = ''
        self.service = 0
        self.flex = 0
        self.fundraising = 0
        self.attendance = 0

    # we almost always construct users from json
    @classmethod
    def from_json(cls, document):
        if document == None:
            return None
        
        user = cls(document.get('email'))
        user.id = document.get('_id', None)
        user.first_name = document.get('first_name', '')
        user.last_name = document.get('last_name', '')
        user.service = document.get('service', 0)
        user.flex = document.get('flex', 0)
        user.fundraising = document.get('fundraising', 0)
        user.attendance = document.get('attendance', 0)
        return user
    
    # dump user back to json
    def dump(self):
        document = {'email': self.email,
                    'first_name': self.first_name, 
                    'last_name': self.last_name,
                    'service': self.service,
                    'flex': self.flex,
                    'fundraising': self.fundraising,
                    'attendance': self.attendance}
        if self.id:
            document['_id'] = ObjectId(id)
        return document

# -----------------------------------------------------------------------

class Event():
    # completely default constructor
    def __init__(self):
        self.id = None
        self.name = ''
        self.creator = ''
        self.value = 0
        self.category = ''
        self.location = ''
        self.users = []
        self.closed = False

    # we almost always construct events from json
    @classmethod
    def from_json(cls, document):
        if document == None:
            return None
        
        event = cls()
        event.id = document.get('_id', None) # we don't want to raise an error on no id
        event.name = document['name']
        event.creator = document['creator']
        event.value = document['value']
        event.category = document['category']
        event.location = document['location']
        event.users = document['users']
        event.closed = document['closed']
        return event
    
    # dump event back to json
    def dump(self):
        document = {'name': self.name,
                    'creator': self.creator, 
                    'value': self.value,
                    'category': self.category,
                    'location': self.location,
                    'users': self.users,
                    'closed': self.closed}
        if self.id:
            document['_id'] = ObjectId(id)
        return document