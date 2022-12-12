# connect to mongodb
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
from qrGen import generateQR
from dotenv import load_dotenv
from idGen import idGen
import os

app = Flask(__name__, template_folder='template', static_folder='static')

load_dotenv()

# load db url from .env file
db_url = os.environ.get('MONGO_LINK')

# connect to mongodb Customer_Identifier database
client = MongoClient(db_url)
db = client.Customer_Identifier

# Load Collection Customer
Customer = db.Customer

# Load Collection Sales Rep
SalesRep = db.SalesRep

# Load Collection Product
product = db.Product

# Load Collection DeviceFingerprint
DeviceFingerprint = db.DeviceFingerprint


# Session Config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super'


# API CALLS CODE

###########################################################################################################################

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('name', None)
    session.clear()
    return redirect(url_for('index'))


# SALES MANAGEMENT CODE

@app.route('/sales/loginAPI', methods=['POST'])
def salesLoginAPI():
    phone = request.form["phone"]
    password = request.form["password"]
    if SalesRep.find_one({"phone": phone, "password": password}):
        # get user name from db
        data = SalesRep.find_one({"phone": phone, "password": password})
        name = data['name']
        id = data['_id']
        session['id'] = str(id)
        session['name'] = name
        return redirect(url_for('salesHome'))
    else:
        return redirect(location=url_for('salesLogin', message="Wrong Username or Password"))


@app.route('/sales/signUp', methods=['POST'])
def salesSignUp():
    # get user phone number name from request
    data = request.get_json()
    # check if user already exists
    if SalesRep.find_one({"phone": data['phone']}):
        return jsonify({"message": "User Already Exists"})
    else:
        # TODO: Return Sign Up Page for sales rep
        return jsonify({"message": "Welcome Sales Rep"})

    
@app.route('/getCustomer/qrCode', methods=['GET'])
def customerQR():
    if(session.get('id') is not None):
        # generate QR code
        rep_id = session.get('id')
        return generateQR(rep_id)





@app.route('/getCustomer/userdata', methods=['POST'])
def getUserData():
    # TODO: get user data from the session id of the user and return it to the Sales Rep
    pass


@app.route('/getCustomer/setAnon', methods=['POST'])
def setAnon():
    data = request.get_json()
    # print(data)
    # check if user already exists
    if DeviceFingerprint.find_one({"_id": data['_id']}):
        return jsonify({"message": "User Already Exists"})

    DeviceFingerprint.insert_one({"_id": data['_id'], 
                        "deviceName": data['deviceName'], 
                        "deviceOS": data['deviceOS'], 
                        "ipAddress": data['ipAddress'], 
                        "geoLocation": data['geoLocation']})
    return jsonify({"message": "Success"})


@app.route('/testAPI', methods=['GET', 'POST'])
def testAPI():
    data = str(request.get_json())
    print(data)
    return jsonify({"message": "Success"})


# CUSTOMER MANAGEMENT CODE


@app.route('/getCustomer', methods=['POST'])
def getCustomer():
    # get phone number from the form
    data = str(request.form["phone"])
    # check if user already exists
    if Customer.find_one({"phone": data}):
        # get user name from db
        # name = Customer.find_one({"phone": data['phone']})['name']
        return redirect(url_for('login'))
    else:
        # TODO: Return Sign Up Page
        return redirect(url_for('registrationRender', phone=data))



@app.route('/getCustomer/signUp', methods=['POST'])
def signUp():
    # get phone, email, address, name, password from the form
    data = request.form
    # generate random id
    id = idGen()
    # check if ID used
    while not(Customer.find({"_id": id})):
        id = idGen()
    
    # add user to db
    Customer.insert_one({"_id": id, 
                        "phone": data['phone'], 
                        "email": data['email'], 
                        "address": data['address'], 
                        "name": data['name'], 
                        "password": data['password']})
    return redirect(url_for('login'))


# customer Login

@app.route('/getCustomer/loginApi', methods=['POST'])
def loginApi():
    # get phone and password from the form
    phone = request.form["phone"]
    password = request.form["password"]
    if Customer.find_one({"phone": phone, "password": password}):
        # get user name from db
        data = Customer.find_one({"phone": phone, "password": password})
        name = data['name']
        id = data['_id']
        return render_template("message.html", message="Welcome Back " + name+" "+str(id))
    else:
        return redirect(location=url_for('login', message="Wrong Username or Password"))


# WEB RENDER CODE

###########################################################################################################################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/bangles')
def bangles():
    return render_template('bangles_catalogue.html')

@app.route('/jewellery')
def jewellery():
    return render_template('jewellery.html')

# THis only renders the page the login handler written in api calls code handles the request
# this checks the phone number and returns the login page if already registered
# else returns the registration page
@app.route('/login',methods=['GET'])
def logCheck():
    return render_template('logCheck.html')

@app.route('/getCustomer/login',methods=['GET'])
def login():
    if request.args.get('message'):
        message = request.args.get('message')
        return render_template('login.html', message=message)
    return render_template('login.html')

@app.route('/registration',methods=['GET'])
def registrationRender():
    data = request.args.get('phone')
    return render_template('registration.html', phone=data)

@app.route('/sales/login',methods=['GET'])
def salesLogin():
    if request.args.get('message'):
        message = request.args.get('message')
        return render_template('salesLogin.html', message=message)
    return render_template('salesLogin.html')


@app.route('/sales/home', methods=['GET','POST'])
def salesHome():
    if(session.get('id') is not None):
        # get sales rep info from db
        data = SalesRep.find_one({"_id": session.get('id')})

        return render_template("salesHome.html", SalesRep=data)
    else:
        return redirect(url_for('salesLogin'))


if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True,host="0.0.0.0")
