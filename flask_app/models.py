from flask import jsonify, Response
from flask_login import UserMixin
from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId

# only here so this can be imported in multiple blueprints after being instantiated once
# in __init__.py
mongo = PyMongo()

class Model(dict):
    """Basic Model for MongoDB

    Adapted from https://gist.github.com/fatiherikli/4350345
    """
    __getattr__ = dict.get
    # __delattr__ = dict.__delitem__
    # __setattr__ = dict.__setitem__

    def save(self):
        if self.is_loaded(): 
            self.collection.update({'_id': ObjectId(self._id) }, self) #pylint: disable=E0203
        else:
            self._id = str(self.collection.insert(self))

    def load(self, key='_id'):
        try: 
            if key == '_id':
                self.update(self.collection.find_one({'_id': ObjectId(self._id)}))
            else:
                self.update(self.collection.find_one({key: self.__getattr__(key)}))
            return True
        except:
            return False

    def remove(self):
        if self.is_loaded():
            self.collection.remove({'_id': ObjectId(self._id)})
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

    def __init__(self):
        super(User, self).__init__({
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_officer': False,
            'attendance': 0,
            'service': 0,
            'flex': 0,
            'fundraising': 0
        })

class Event(Model):
    """Event model for MongoDB
    """
    collection = MongoClient()['data']['events']

    def __init__(self):
        super(Event, self).__init__({
            'name': '',
            'creator': '',
            'category': 'flex',
            'value': 0,
            'location': '',
            'shifts': False,
            'info': '',
            'users': [],
            'closed': False
        })
