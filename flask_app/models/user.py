import time
from operator import sub

import flask_bcrypt
from flask import flash, session

from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
import re

from flask_mail import Mail, Message

mail = Mail(app)

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app.config['MAIL_SERVER'] = 'smtp-relay.sendinblue.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'aklusa02@yandex.ru'
app.config[
    'MAIL_PASSWORD'] = 'xsmtpsib-8030c7d67a90973584f9aebb47ac48fb8ca1fb691c302a2bfeb4e087447ed55d-wS2GvBpKtWbmA3zs'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

dbname = 'licenses'


# model the class after the friend table from our database
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "select * from users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(dbname).query_db(query)
        # Create an empty list to append our instances of friends
        userlist = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            userlist.append(cls(user))
            print(user)
        return userlist

    @classmethod
    def createusr(self, data):
        pswhash = bcrypt.generate_password_hash(data['password'])

        query = f'insert into users(first_name, last_name, email, username, password, created_at, updated_at) values(%(first_name)s,%(last_name)s,%(email)s, %(username)s, "{pswhash}", now(), now());'

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def dropuser(self, data):
        query = "delete from users where id=%(id)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def getuser(cls, data):
        query = "select * from users where email=%(email)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return send[0]

    @classmethod
    def checkemail(cls, data):

        query = "select email from users where email=%(email)s;"

        send = connectToMySQL(dbname).query_db(query, data)
        print(send)
        return send

    @classmethod
    def emailexists(cls, data):
        emailExists = True
        query = "select email from users where email=%(email)s;"
        send = connectToMySQL(dbname).query_db(query, data)

        if len(send) == 0:
            emailExists = False

        return emailExists

    @classmethod
    def userexists(cls, data):
        query = "select username from users where username=%(username)s;"

        send = connectToMySQL(dbname).query_db(query, data)
        print(send)
        return send

    @classmethod
    def savechanges(self, data):
        query = "update users set first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at=now() where id=%(userid)s"

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def login(cls, data):

        isApproved = False

        query = "select id, first_name, email, username, password from users where email=%(email)s;"
        send = connectToMySQL(dbname).query_db(query, data)
        ehash = send[0]['password']
        isApproved = bcrypt.check_password_hash((ehash[2:len(ehash) - 1]), data['password'])

        if isApproved == True:
            session['first_name'] = send[0]['first_name']
            session['user_id'] = send[0]['id']

        return isApproved

    @classmethod
    def updatepasswordwithkey(cls, data):

        pswhash = bcrypt.generate_password_hash(data['password'])

        query = f'update users set password = "{pswhash}" where reset_key =%(reset_key)s'

        send = connectToMySQL(dbname).query_db(query, data)

        return send

    @classmethod
    def checktoken(cls, data):
        is_valid = True
        query = 'select reset_key from users where reset_key=%(token)s'

        send = connectToMySQL(dbname).query_db(query, data)

        if len(send) < 1:
            is_valid = False

        return is_valid

    @classmethod
    def makekey(cls, data):

        query = f'update users set reset_key = %(token)s  where email =%(email)s'

        send = connectToMySQL(dbname).query_db(query, data)
        return send

    @classmethod
    def counter(cls, data):
        User.makekey(data)
        t = 300
        while t:
            mins, secs = divmod(t, 30)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

        print('Fire in the hole!!')

    @staticmethod
    def regvalidate(data):
        is_valid = True
        if len(User.checkemail(data)) > 0:
            flash(u"Email Already Exists", 'reg')
            print("Email Exists")
            is_valid = False
        if len(User.userexists(data)) > 0:
            flash(u"Username Exists", 'reg')
            print("Username Exists")
            is_valid = False
        if len(data['first_name']) < 3:
            flash(u"Name is too short", 'reg')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash(u"Invalid Email Address", 'reg')
        if data['password'] != data['confirm-password']:
            is_valid = False
            flash(u"Passwords Don't match", 'reg')
        return is_valid

    @staticmethod
    def loginvalidate(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash(u"Email isn't valid", 'login')
            is_valid = False

        if not User.emailexists(data):
            flash(u"Not a valid user", 'login')
            is_valid = False

        return is_valid

    @staticmethod
    def sendemail(data):
        msg = Message("Hyperlink Account Password Reset", sender="no-reply@hyperlink-network.com",
                      recipients=[f"{data['email']}"])
        msg.body = f'Your account password reset link is https://licensesystem.hyperlink-network.com/reset/{data["token"]}'
        mail.send(msg)
        return "Sent"

    @staticmethod
    def resetvalidate(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
        if not User.emailexists(data):
            is_valid = False
        if data['password'] != data['confirm-password']:
            is_valid = False
            flash(u"Passwords Don't match", 'mkpass')
        return is_valid
