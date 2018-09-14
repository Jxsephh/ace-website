from flask_login import UserMixin
from flask_pymongo import PyMongo

mongo = PyMongo()

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.first_name = ''
        self.last_name = ''
        self.attendance = 0
        self.service = 0
        self.flex = 0
        self.fundraising = 0

    @classmethod
    def from_json(cls, document):
        if document == None:
            return None
        assert document['_type'] == 'user'
        
        user = cls(document['id'])
        user.first_name = document.get('first_name', '')
        user.last_name = document.get('last_name', '')
        user.attendance = document.get('attendance', 0)
        user.service = document.get('service', 0)
        user.flex = document.get('flex', 0)
        user.fundraising = document.get('fundraising', 0)
        return user
    
    def dump(self):
        return {'_type': 'user', 
                'id': self.id,
                'first_name': self.first_name, 
                'last_name': self.last_name,
                'attendance': self.attendance,
                'service': self.service,
                'flex': self.flex,
                'fundraising': self.fundraising}