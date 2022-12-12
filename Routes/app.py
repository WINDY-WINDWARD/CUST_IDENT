# connect to mongodb
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from flask import Flask, request, jsonify, render_template, redirect, url_for
from qrGen import generateQR
from dotenv import load_dotenv
from idGen import idGen
import os

app = Flask(__name__, template_folder='template', static_folder='static')

load_dotenv()

load db url from .env file
db_url = os.environ.get('MONGO_LINK')

connect to mongodb Customer_Identifier database
client = MongoClient(db_url)
db = client.Customer_Identifier

Load Collection Customer
Customer = db.Customer

Load Collection Sales Rep
SalesRep = db.SalesRep

Load Collection Product
product = db.Product

Load Collection DeviceFingerprint
DeviceFingerprint = db.DeviceFingerprint





# API CALLS CODE

###########################################################################################################################


@app.route('/salesLogin', methods=['POST'])
def salesLogin():
    # get username and password from request
    data = request.get_json()
    # check if user exists
    if SalesRep.find_one({"user": data['user'], "password": data['password']}):
        # get user name from db
        name = SalesRep.find_one({"user": data['user'], "password": data['password']})['name']
        # get user id from db
        id = SalesRep.find_one({"user": data['user'], "password": data['password']})['_id']
        return jsonify({"message": "Welcome Back {}".format(name), "id": str(id)})
    else:
        return jsonify({"message": "Wrong Username or Password"})


@app.route('/salesSignUp', methods=['POST'])
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
    # get sales rep id from request
    data = request.get_json()
    # check if sales rep exists
    if SalesRep.find_one({"_id": ObjectId(data['id'])}): 
        # check perminssion
        if SalesRep.find_one({"_id": ObjectId(data['id'])})['permission'] == "True":
            # generate QR code
            rep_id = str(data['id'])
            return generateQR(rep_id)





@app.route('/getCustomer/userdata', methods=['POST'])
def getUserData():
    # TODO: get user data from the session id of the user and return it to the Sales Rep
    pass





@app.route('/getCustomer', methods=['POST'])
def getCustomer():
    # get phone number from the form
    data = str(request.form["phone"])
    # check if user already exists
    if Customer.find_one({"phone": data}):
        # get user name from db
        # name = Customer.find_one({"phone": data['phone']})['name']
        return render_template("message.html", message="Welcome Back {}".format(data))
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
    return render_template("message.html", message="Welcome {}".format(data['name']))


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
@app.route('/login',methods=['GET'])
def loginRender():
    return render_template('login.html')

@app.route('/registration',methods=['GET'])
def registrationRender():
    data = request.args.get('phone')
    return render_template('registration.html', phone=data)


if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True,host="0.0.0.0")
