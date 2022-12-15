<h1> CodeMafia </h1>


Team Members:
    <ul>
    <li>Karthik Sarode</li>
    <li>Ashish Kumar</li>
    <li>Sasikumar</li>
    <li>Sai Ramana</li>
    </ul>
    
<p>
To run this code:

first install the following dependencies using pip
<ul>
<li>Flask</li>
<li>Flask-SocketIO</li>
<li>Flask-Session</li>
<li>PyQRcode</li>
<li>pymongo</li>
<li>python-dotenv</li>
</ul>

create .env file in the routes directory

setup the following:

note: the project must be hosted on the default 80 port and the domain name shouldnt have a port number
      the socket communication implemented for the production version doesnt support port numbers

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

ISSUE:
we noticed devices with jio 5g connections are assigned IPv6 and the socket implemented is designed to only listen on ipv4 addresses currently, due to the limitations of our hosting provider 
