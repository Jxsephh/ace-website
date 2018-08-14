import datetime
'''
    *  creator
    *  name 	
    *  start/end times 
    *  point value 	
    *  category 	
    *  location 	
    *  users who signed up (emails) 	
    *  closed flag
'''
class Event(object):
    def __init__(self):
        self.owner = None
        self.start_time = None
        self.end_time = None
        self.points = 0
        self.category = None
        self.location = None
        self.sign_up_list = list()

    @property
    def owener(self):
        return self.__owner
    @property
    def start_time(self):
        return self.__start_time
    @property
    def end_time(self):
        return self.__end_time
    @property
    def points(self):
        return self.__points
    @property
    def category(self):
        return self.__category
    @property
    def location(self):
        return self.__location
    def dump(self):
        serialize_dict = dict{}
        serialize_dict['owner'] = self.__owner
        serialize_dict['start_time'] = self.__start_time
        serialize_dict['end_time'] = self.__end_time
        serialize_dict['points'] = self.__points
        serialize_dict['category'] = self.__category
        serialize_dict['location'] = self.__location
        serialize_dict['sign_up_list'] = self.sign_up_list
        return serialize_dict
    def load(self,event_json):
        if 'owner' in event_json:
            self.__owner=event_json['owner']
        if 'start_time' in event_json:
            self.__owner=event_json['start_time']
        if 'end_time' in event_json:
            self.__owner=event_json['end_time']
        if 'points' in event_json:
            self.__owner=event_json['points']
        if 'category' in event_json:
            self.__owner=event_json['category']
        if 'location' in event_json:
            self.__owner=event_json['location']
        if 'sign_up_list' in event_json:
            self.__owner=event_json['sign_up_list']
    

    