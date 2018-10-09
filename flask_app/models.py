from flask import jsonify, Response
from flask_login import UserMixin
from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId

# only here so this can be imported in multiple blueprints after being instantiated once
# in __init__.py
mongo = PyMongo()

class Model(dict):
    """Basic Model for MongoDB

    Taken from https://gist.github.com/fatiherikli/4350345
    """
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self):
        if self._id == None: #pylint: disable=E0203
            self._id = str(self.collection.insert(self))
        else:
            self.collection.update(
                { "_id": ObjectId(self._id) }, self)

    def reload(self):
        if self._id != None:
            self.update(self.collection.find_one({"_id": ObjectId(self._id)}))

    def remove(self):
        if self._id != None:
            self.collection.remove({"_id": ObjectId(self._id)})
            self.clear()

    def is_loaded(self):
        return self._id != None

class User(UserMixin, Model):
    """User model for MongoDB and object used by flask_login
    """
    collection = MongoClient()['data']['users']

    @property
    def id(self):
        return self._id

    def reload(self):
        if self._id != None:
            document = self.collection.find_one({"_id": ObjectId(self._id)})
            if document: 
                self.update(document)
        elif self.email != None:
            document = self.collection.find_one({"email": self.email})
            if document:
                self.update(document)

    @classmethod
    def new_user(cls, email, first_name, last_name):
        return cls({
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'attendance': 0,
            'service': 0,
            'flex': 0,
            'fundraising': 0
        })

class NewEvent(Model):
    """Event model for MongoDB
    """
    collection = MongoClient()['data']['events']

    @property
    def id(self):
        return self._id

    @classmethod
    def new_event(cls, name, creator, category, value, location, info):
        return cls({
            'name': name,
            'creator': creator,
            'category': category,
            'value': value,
            'location': location,
            'info': info,
            'users': [],
            'closed': False
        })

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