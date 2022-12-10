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
        # get user name from db
        name = Customer.find_one({"phone": data['phone']})['name']
        return jsonify({"message": "Welcome Back {}".format(name)})
    else:
        # TODO: Return Sigu Up Page
        return jsonify({"message": "Welcome to our app"})



if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)
