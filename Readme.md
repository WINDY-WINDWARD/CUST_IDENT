<h1> Hello World </h1>

<h2> TO-DO: </h2>

make login.html, registration.html, logcheck.html, salesLogin, salesDashboard beautiful

add session and integrate socket io for QR generation and dashboard redirect for sales rep

add cookie check and cookie creation for customer on all pages



data structure for Customer login/signup
```
{
    "_id":"Value",
    "name":"Value",
    "email":"Value",
    "phone":"Value",
    "address": "Value"
}


```

Product Data structure

```

{
    "_id": "Value",
    "name": "Value",
    "CategoryID": "Value",
    "Description": "Value",
    "price":"Value"
}

```

SalesRep Data structure

```

{
    "_id": "Value",
    "name": "Value",
    "permission": "Value",
    "phone":"Value",
    "email":"Value"
}

```
DeviceFingerprinting Data structure

```

{
    "_id": "Value",
    "deviceName": "Value",
    "deviceOS": "Value",
    "ipAddress":"Value",
    "geoLocation":"Value"
}

```
DataStream data structure

```

{
    "_id":"Value",
    "data": {"value":"Value"},
    "timestamp":"Value"
}

```
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


Product Log
```
{'_id': 'Wb4SHxNOQW9C3gli1ZbU', 
 'data': {'CatgoryID': 'category_2', 
 'ProductID': 'prod_4'}, 
 'timestamp': '1670910297343'
 }

```

```