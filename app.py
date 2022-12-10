# connect to mongodb
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# load db url from .env file
db_url = os.environ.get('MONGO_LINK')

# connect to mongodb Customer_Identifier database
client = MongoClient(db_url)
db = client.Customer_Identifier

# Load Collection Customer
Customer = db.Customer


@app.route("/")
def hello():
    return "Hello World!"



@app.route('/signUp', methods=['POST'])
def signUp():
    # get user phone number name from request
    data = request.get_json()
    # check if user already exists
    if Customer.find_one({"phone": data['phone']}):
        return jsonify({"message": "User already exists"})
    # insert user in db
    Customer.insert_one(data)

    return jsonify({"message": "User created successfully"})



@app.route('/login', methods=['POST'])
def login():
    # get user phone number name from request
    data = request.get_json()
    # get user from db
    user = Customer.find_one({"phone": data['phone']})
    return dumps(user)


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
