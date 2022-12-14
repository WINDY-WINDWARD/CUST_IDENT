<h1> CodeMafia </h1>
Team Members:
    Karthik Sarode
    Ashish Kumar
    Sasikumar
    Sai Ramana

<br>
To run this code:

first install the following dependencies using pip

Flask
Flask-SocketIO
Flask-Session
PyQRcode
pymongo
python-dotenv


create .env file in the routes directory

setup the following:

note: the project must be hosted on the default 80 port and the domain name shouldnt have a port number

```

MONGO_LINK = '<your mongo link>'

WEB_PAGE = '<the domain name>'

```


Setup your Mongo with the following

Create Database

```
<Database>
Customer_Identifier
            <collections>
            Customer
            SalesRep
            Stitch
            DeviceFingerprint
            DataStream
```

<h2>The following is the Structure for Mongo Collections</h2>
<h2> data structure for Customer/SalesRep </h2>

```
{
    "_id":"Value",
    "name":"Value",
    "email":"Value",
    "phone":"Value",
    "address": "Value"
}
```

<h2>Stitch data structure</h2>
_id added automatically by db

```
{
    "deviceID": "value"
    "customerID": "value"
}
```

<h2>DataStream data structure</h2>

```

{
    "_id":"Value",
    "data": {"value":"Value"},
    "timestamp":"Value"
}

```

<h2>Device Fingerprint</h2>
Complete User Information When cookie created (setAnon)

```
{
  "_id": "DJTDwJeVDi4N3y34yloc", 
  "ipaddress": "27.7.135.55", 
  "geoLocation": "Mysore", 
  "os": {
      "os": "Windows", 
      "osVersion": "10"
      }, 
  "Browser": {
      "browser": "Chrome", 
      "browserVersion": "108.0.0"
    }, 
  "Incognito": "False"
}

```
