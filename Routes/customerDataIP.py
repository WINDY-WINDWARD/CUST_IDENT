
# from pymongo import MongoClient
# # from bson.objectid import ObjectId
# # from bson.json_util import dumps
# # from bson.json_util import loads
# # from flask import Flask, request, jsonify, render_template, redirect, url_for, session
# # from flask_socketio import SocketIO, emit, join_room, leave_room
# # from flask_session import Session
# # from qrGen import generateQR
# from dotenv import load_dotenv
# # from idGen import idGen
# import os
# # from customerDataIP import getCustomersIP
# # import logging

# # app = Flask(__name__, template_folder='template', static_folder='static')

# load_dotenv()

# #remove later
# # log = logging.getLogger('werkzeug')
# # log.setLevel(logging.ERROR)

# # load db url from .env file
# db_url = os.environ.get('MONGO_LINK')

# # connect to mongodb Customer_Identifier database
# client = MongoClient(db_url)
# db = client.Customer_Identifier

# # Load Collection Customer
# Customer = db.Customer

# # Load Collection Sales Rep
# SalesRep = db.SalesRep

# # Load Collection Product
# product = db.Product

# stitch = db.Stitch

# # Load Collection DeviceFingerprint
# DeviceFingerprint = db.DeviceFingerprint

# # Load Collection DataStream
# DataStream = db.DataStream


def getCustomersIP(ip,DeviceFingerprint,stitch,DataStream):
# def getCustomersIP(ip):

    # get all Did with same IP
    Devices = DeviceFingerprint.find({"ipaddress":ip})
    # get all Customer with same IP
    ids = []
    for Device in Devices:
        ids.append(Device["_id"])
    # print(ids)

    # get all stitch with same ids
    customersID = []
    for i in ids:
        if stitch.find_one({"deviceID":i}) != None:
            # print(stitch.find_one({"deviceID":id}))
            # print(DataStream.find_one({"Did":id}))
            if DataStream.find_one({"Did":i}):
                customersID.append(i)
            
    print(customersID)
    return customersID




# getCustomersIP("115.99.144.124")