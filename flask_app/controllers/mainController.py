import time

from flask import render_template, session, request, redirect, flash
from flask_app import app
from flask_app.models import user, apikeys, licensekeys
from random import random, randrange, randint
import time


@app.route("/")
def mainPage():
    session['logged_in'] = False
    session['user_id'] = ""
    session['license_id'] = ""
    session['api_id'] = ""
    session['viewingLicenses'] = False
    session['revokeProcess'] = False
    session['reset_token'] = ""

    return render_template("homepage.html")


@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/makeuser", methods=['POST', 'GET'])
def mkuser():
    data = {"first_name": request.form['first_name'], "last_name": request.form['last_name'],
            "email": request.form['email'], "username": request.form['username'], "password": request.form['password'],
            "confirm-password": request.form['confirm-password']}
    if not user.User.regvalidate(data):
        return redirect("register")
    else:
        user.User.createusr(data)
        return redirect("login")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect("/")


@app.route("/processlogin", methods=['GET', 'POST'])
def processlogin():
    data = {"email": request.form['email'], "password": request.form['password']}
    if not user.User.loginvalidate(data):
        return redirect("/login")
    elif not user.User.login(data):
        flash(u"Login has failed", 'login')
        return redirect("/login")
    else:
        session['logged_in'] = True
        return redirect("dashboard")


@app.route("/dashboard")
def dashboard():
    session['api_id'] = ""
    data = {"user_id": session['user_id']}
    apilist = apikeys.Api_Keys.get_all(data)
    session['viewingLicenses'] = False
    if not session['logged_in']:
        return redirect("/login")
    else:
        return render_template("dashboard.html", apilist=apilist)


@app.route("/toggleviewlicense", methods=['POST', 'GET'])
def viewlicense():
    if not session['viewingLicenses']:
        session['viewingLicenses'] = True
        session['api_id'] = request.form['apikey_id']

        return redirect("/licensekeys")
    else:
        session['viewingLicenses'] = False
        session['api_id'] = ""
        return redirect("/dashboard")


@app.route("/licensekeys")
def showkeys():
    if not session['viewingLicenses']:
        return render_template("404.html")
    else:

        data = {"apikey_id": session['api_id']}
        lic = licensekeys.License_Keys.get_all(data)
        product_name = apikeys.Api_Keys.getapikey(data)
        return render_template("licenses.html", lic=lic, product_name=product_name)


@app.route("/makeproduct")
def makeproduct():
    if not session['logged_in']:
        return redirect("/login")
    else:
        return render_template("createproduct.html")


@app.route("/createproduct", methods=['GET', 'POST'])
def createproduct():
    makeapikey = randint(100000000, 999999999)
    data = {"product_name": request.form['product_name'], "apikey": f"api-{makeapikey}", "user_id": session['user_id']}

    if not apikeys.Api_Keys.validatecreation(data):
        return redirect("/makeproduct")
    else:
        apikeys.Api_Keys.createapikey(data)
        return redirect("/dashboard")


@app.route("/deleteproduct", methods=['GET', 'POST'])
def deleteproduct():
    data = {'api_key': request.form['apikey_id_del']}
    apikeys.Api_Keys.dropapikey(data)
    return redirect("/dashboard")


@app.route("/makelicense")
def makelicense():
    if not session['logged_in']:
        return redirect("/")
    else:
        return render_template("createlicense.html")


@app.route("/createlicense", methods=['GET', 'POST'])
def createlicense():
    makelicensekey = randint(100000000, 999999999)
    data = {"license_key": f"LIC-{makelicensekey}", "server_ip": request.form['server_ip'],
            "apikey_id": session['api_id']}
    licensekeys.License_Keys.createlicensekey(data)

    return redirect("/licensekeys")


@app.route("/revokelicense", methods=['GET', 'POST'])
def revoke():
    data = {"license_key": request.form['license_key']}
    licensekeys.License_Keys.droplicensekey(data)
    return redirect("/licensekeys")


@app.route("/request_reset_password")
def resetpasspage():

    return render_template("resetpass.html")

@app.route("/sendtoken", methods=['GET', 'POST'])
def resetfunc():
    rs_token = randint(100000000, 999999999)
    data = {"email": request.form['email'], "token": rs_token}
    if not user.User.checkemail(data):
        return redirect("/request_reset_password")
    else:
        user.User.makekey(data)
        user.User.sendemail(data)
    flash(u"Check your email for password reset link", 'resetpass')
    return redirect("/request_reset_password")

@app.route("/reset/<string:token>")
def passchangepage(token):

    data = {"token": token}

    if not user.User.checktoken(data):
        return redirect("/request_reset_password")
    else:
        return render_template("createnewpassword.html", token=token)

@app.route("/updatepass", methods=['GET','POST'])
def updatepass():

    data = {}


    return




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


