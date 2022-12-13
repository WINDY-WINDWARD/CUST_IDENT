# connect to mongodb
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session
from qrGen import generateQR
from dotenv import load_dotenv
from idGen import idGen
import os
from customerDataIP import getCustomersIP
import logging

app = Flask(__name__, template_folder='template', static_folder='static')

load_dotenv()

#remove later
log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

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

stitch = db.Stitch

# Load Collection DeviceFingerprint
DeviceFingerprint = db.DeviceFingerprint

# Load Collection DataStream
DataStream = db.DataStream


# Session Config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super'
Session(app)

# SocketIO Config
socketio = SocketIO(app, manage_session=False, cors_allowed_origins="*")


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


# @app.route('/sales/signUp', methods=['POST'])
# def salesSignUp():
#     # get user phone number name from request
#     data = request.get_json()
#     # check if user already exists
#     if SalesRep.find_one({"phone": data['phone']}):
#         return jsonify({"message": "User Already Exists"})
#     else:
#         # TODO: Return Sign Up Page for sales rep
#         return jsonify({"message": "Welcome Sales Rep"})

    
@app.route('/getCustomer/qrCode', methods=['GET'])
def customerQR():
    if(session.get('id') is not None):
        # generate QR code
        rep_id = session.get('id')
        return generateQR(rep_id)





@app.route('/getCustomer/setUserData', methods=['POST'])
def getUserData():
    data = request.get_json()
    DataStream.insert_one({"Did": data['_id'],
                            "data": data['data'],
                            "timestamp": data['timestamp']})
    return jsonify({"message": "Success"})


@app.route('/getCustomer/setAnon', methods=['POST'])
def setAnon():
    data = request.get_json()
    if DeviceFingerprint.find_one({"_id": data['_id']}):
        return jsonify({"message": "Session Already Exists"})
    else:
        DeviceFingerprint.insert_one({"_id": data['_id'], 
                            "ipaddress": data['ipaddress'], 
                            "geoLocation": data['geoLocation'], 
                            "os": data['os'], 
                            "Browser": data['Browser'], 
                            "Incognito": data['Incognito']})
        return jsonify({"message": "Success"})


@app.route('/testAPI', methods=['GET', 'POST'])
def testAPI():
    data = str(request.get_json())
    print(data)
    return jsonify({"message": "Success"})




# CUSTOMER MANAGEMENT CODE
@app.route('/getCustomer', methods=['GET', 'POST'])
def getCustomer():
    if request.method == 'POST':
        # get phone number from the form
        data = str(request.form["phone"])
        # salesRepId = str(request.args.get('key'))
        # check if user already exists
        if Customer.find_one({"phone": data}):
            # get user name from db
            # name = Customer.find_one({"phone": data['phone']})['name']
            return redirect(url_for('login'))
        else:
            # TODO: Return Sign Up Page
            return redirect(url_for('registrationRender', phone=data))
    elif(request.method == 'GET'):
        room = request.args.get('key')
        session['room'] = room
        session['deviceID'] = request.cookies.get('userFingerPrint')
        deviceID = session['deviceID']
        # print(deviceID)
        return render_template('customerLogin.html', session=session, deviceID=deviceID)




@app.route('/getCustomer/signUp', methods=['GET', 'POST'])
def signUp():
    # get phone, email, address, name, password from the form
    data = request.form
    deviceID = request.cookies.get('userFingerPrint')
    # generate random id
    id = idGen()
    # check if ID used
    while not(Customer.find({"_id": id})):
        id = idGen()
    
    # add user to db
    if Customer.find_one({"phone": data['phone']}):
        return redirect(url_for('login'))
    Customer.insert_one({"_id": id, 
                        "phone": data['phone'], 
                        "email": data['email'], 
                        "address": data['address'], 
                        "name": data['name'], 
                        "password": data['password']})
    stitch.insert_one({"customerID": id, 
                        "deviceID": deviceID})
    return redirect(url_for('login'))


# customer Login

@app.route('/getCustomer/loginApi', methods=['POST'])
def loginApi():
    # get phone and password from the form
    phone = request.form["phone"]
    password = request.form["password"]
    if Customer.find_one({"phone": phone, "password": password}):
        # get user name from db
        # data = Customer.find_one({"phone": phone, "password": password})
        # name = data['name']
        # id = data['_id']
        # return render_template("message.html", message="Welcome Back " + name+" "+str(id))
        return redirect(url_for('index'))
    else:
        return redirect(location=url_for('login', message="Wrong Username or Password"))


@app.route('/salesDash', methods=['GET'])
def salesDash():
    # TODO: USING COOKIE MODIFY TO WORK WITH SESSION AND SALES REP ID + COOKIE
    if session.get('id') is not None:
        fuckid = request.args.get('user')
        # print(id)
        # if fuckid is None:
        #     ip = request.session['ip']
        #     ipdata = getCustomersIP(ip,DeviceFingerprint,stitch,DataStream)
        #     if len(ipdata) == 0:
        #         return render_template("salesDashboard.html", data=None, customerData=None)
        #     elif len(ipdata) == 1:
        #         fuckid = ipdata[0]
        #         data = DataStream.find({"Did": fuckid})
        #         # print(data)
        #         if stitch.find_one({"deviceID": fuckid}):
        #             customerID = stitch.find_one({"deviceID": fuckid})['customerID']
        #             # print(customerID)
        #             customerData = Customer.find_one({"_id": customerID})
        #             # print(customerData)
        #             return render_template("salesDashboard.html", data=data, customerData=customerData)
        #             # return render_template("salesDashboard.html", data=data, customerData=None)
        #         else:
        #             return render_template("salesDashboard.html", data=data,customerData=None)
        #     elif len(ipdata) > 1:
        #         data = []
        #         customerData = []
        #         for i in ipdata:
        #             data.append(DataStream.find({"Did": i}))
        #             if stitch.find_one({"deviceID": fuckid}):
        #                 customerID = stitch.find_one({"deviceID": fuckid})['customerID']
        #                 # print(customerID)
        #                 customerData.append(Customer.find_one({"_id": customerID}))
        #                 # print(customerData)
        #             else:
        #                 customerData.append(None)
        #         return render_template("salesDashboardMulti.html", data=data, customerData=customerData)

        data = None
        if DataStream.find_one({"Did": fuckid}):
            data = list(DataStream.find({"Did": fuckid}))
            print(data)
            if stitch.find_one({"deviceID": fuckid}):
                customerID = stitch.find_one({"deviceID": fuckid})['customerID']
                # print(customerID)
                customerData = Customer.find_one({"_id": customerID})
                # print(customerData)
                return render_template("salesDashboard.html", data=data, customerData=customerData)
                # return render_template("salesDashboard.html", data=data, customerData=None)
            else:
                return render_template("salesDashboard.html", data=data,customerData=None)
        return render_template("salesDashboard.html", data=data,customerData=None)
        
    else:
        return redirect(url_for('login'))





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

@app.route('/product')
def product():
    return render_template('product.html')

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
        session['room'] = session.get('id')
        session['deviceId'] = request.cookies.get('userFingerPrint')
        return render_template("salesHome.html", SalesRep=data, session=session)
    else:
        return redirect(url_for('salesLogin'))

# SOCKETIO CODE

###########################################################################################################################

@socketio.on('join', namespace='/sales')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('deviceId')}, room=room)

@socketio.on('text', namespace='/sales')
def text(message):
    room = session.get('room')
    emit('message', {'msg': message['msg']}, room=room)

@socketio.on('left', namespace='/sales')
def left(message):
    room = session.get('room')
    useername = session.get('deviceId')
    leave_room(room)
    emit('status', {'msg': session.get('id')}, room=room)

if __name__ == "__main__":
    # socketio.run(app, threaded=True, port=5000, debug=True,host="0.0.0.0")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
