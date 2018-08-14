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


class User(object):
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email = None
        self.service = 0
        self.flex = 0
        self.fundraising = 0
        self.permission = 0
    @property
    def first_name(self):
        return self.__first_name
    @first_name.setter
    def first_name(self,first_name):
        self.__first_name = first_name

    @property
    def last_name(self):
        return self.__last_name
    @last_name.setter
    def last_name(self,last_name):
        self.__last_name = last_name

    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self,email):
        self.__email = email

    @property
    def service(self):
        return self.__service
    @service.setter
    def service(self,service):
        if service<0:
            self.__service = 0
        else:
            self.__service = service

    @property
    def flex(self):
        return self.__flex
    @flex.setter
    def flex(self,flex):
        if flex<0:
            self.__flex = 0
        else:
            self.__flex = flex
    
    @property
    def fundraising(self):
        return self.__fundraising
    @fundraising.setter
    def fundraising(self,fundraising):
        if fundraising<0:
            self.__fundraising = 0
        else:
            self.__fundraising = fundraising
    
    def dump(self):
        serlizie_user = dict()
        serlizie_user['first_name']=self.first_name
        serlizie_user['last_name']=self.last_name
        serlizie_user['email']=self.email
        serlizie_user['service']=self.service
        serlizie_user['flex']=self.flex
        serlizie_user['fundraising']=self.fundraising
        serlizie_user['permission']=self.permission
        return serlizie_user
    def load(self,decode):
        if 'first_name' in decode:
            self.first_name = decode['first_name']
        if 'last_name' in decode:
            self.last_name = decode['last_name']
        if 'email' in decode:
            self.email = decode['email']
        if 'service' in decode:
            self.service = decode['service']
        if 'flex' in decode:
            self.flex = decode['flex']
        if 'fundraising' in decode:
            self.fundraising = decode['fundraising']
        if 'permission' in decode:
            self.permission = decode['permission']
        

    
    
    

