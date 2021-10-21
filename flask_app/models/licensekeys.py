from operator import sub

import flask_bcrypt
from flask import flash, session

from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

dbname = 'licenses'


# model the class after the friend table from our database
class License_Keys:
    def __init__(self, data):
        self.id = data['id']
        self.license_key = data['license_key']
        self.server_ip= data['server_ip']
        self.api_key_id = data['api_key_id']

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls, data):
        query = "select * from license_keys where api_key_id=%(apikey_id)s;"
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
    def createlicensekey(self, data):

        query = f'insert into license_keys(license_key, server_ip, api_key_id) values(%(license_key)s, %(server_ip)s, %(apikey_id)s);'

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def droplicensekey(self, data):
        query = "delete from license_keys where license_key=%(license_key)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def droplicensekeybulk(self, data):
        query = "delete from license_keys where api_key_id=%(api_key)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def getlicensekey(cls, data):
        query = "select * from license_keys where api_key_id=%(apikey_id)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return send[0]
