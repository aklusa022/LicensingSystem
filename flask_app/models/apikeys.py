from operator import sub

import flask_bcrypt
from flask import flash, session

from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
import re

from flask_app.models import licensekeys

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

dbname = 'licenses'


# model the class after the friend table from our database
class Api_Keys:
    def __init__(self, data):
        self.id = data['id']
        self.api_key = data['apikey']
        self.product_name = data['product_name']
        self.user_id = data['user_id']

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls, data):
        query = "select * from api_keys where user_id=%(user_id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(dbname).query_db(query, data)
        # Create an empty list to append our instances of friends
        apikey_list = []
        # Iterate over the db results and create instances of friends with cls.
        for key in results:
            apikey_list.append(cls(key))
            print(key)
        return apikey_list

    @classmethod
    def createapikey(self, data):
        query = f'insert into api_keys(apikey, product_name, user_id) values(%(apikey)s, %(product_name)s, %(user_id)s);'

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def dropapikey(self, data):
        licensekeys.License_Keys.droplicensekeybulk(data)
        query = "delete from api_keys where id=%(api_key)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return send

    @classmethod
    def getapikey(cls, data):

        query = "select * from api_keys where id=%(apikey_id)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return send[0]


    @staticmethod
    def validatecreation(data):
        is_valid = True
        if len(data['product_name']) < 3:
            flash(u"Product name must be atleast 3 characters", "makeproduct")
            is_valid = False


        return is_valid

