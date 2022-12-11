# connect to mongodb
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from flask import Flask, request, jsonify
from qrGen import generateQR
import os

app = Flask(__name__)

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




@app.route("/")
def hello():
    return "Hello World!"





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
def getCustomer():
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



# Test Route for QR Code REMOVE LATER
@app.route('/getCustomer/qrCode1', methods=['GET'])
def getCustomer1():
    return generateQR("test")



@app.route('/getCustomer/signUp', methods=['POST'])
def signUp():
    # get user phone number name from request
    data = request.get_json()
    # check if user already exists
    if Customer.find_one({"phone": data['phone']}):
        # get user name from db
        name = Customer.find_one({"phone": data['phone']})['name']
        return jsonify({"message": "Welcome Back {}".format(name)})
    else:
        # TODO: Return Sign Up Page
        return jsonify({"message": "Welcome to our app"})


if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)
