from pymongo import MongoClient

# connect to mongodb Customer_Identifier database
client = MongoClient("mongodb://localhost:27000/")
db = client.Customer_Identifier

# Load Collection Customer
Customer = db.Customer

data = ([('phone', '9036333248'), ('password', 'QyySSMFJyf3htTw')])

result = Customer.find_one({"phone": data["phone"], "password": "QyySSMFJyf3htTw"})
print(result)