//Cookie Master Functions

let cookieName = "userFingerPrint";
function setCookie(visitorID,User_IP,v_Location,v_OS,v_Browser,v_incognito){
    const d = new Date();
    d.setTime(d.getTime()+(365*24*60*60*1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = `${cookieName} = ${visitorID} ; ${expires}`;
    $.ajax({
      url: '/getCustomer/setAnon',
      type: "POST",
      data: JSON.stringify(
        {"_id": visitorID,
         "ipaddress": User_IP,
         "geoLocation": v_Location,
         "os":v_OS,
         "Browser":v_Browser,
         "Incognito": v_incognito
        }
        ),
      dataType: "json",
      contentType: "application/json",
      });  
    console.log("Cookie Created");
}
function checkCookie(name){
  if(getCookie(name).length<=0){
    return false;
  }
  else{
    return true;
  }
}
function getCookie(cookieName) {
    let name = cookieName + "=";
    let spli = document.cookie.split(';');
    for(var j = 0; j < spli.length; j++) {
      let char = spli[j];
      while (char.charAt(0) == ' ') {
        char = char.substring(1);
      }
      if (char.indexOf(name) == 0) {
        return char.substring(name.length, char.length);
      }
    }
    return "";
  }
// function checkCookie() {
//     var user = getCookie(cookieName);
//     // checking whether user is null or not
//     if (user != "") {
//       return true;
//     }
//     //if user is null
//     else {
//     //   setCookie();
//       return false;
//     }
//   }
  

//Creating the final cookie with user data

  function setDeviceFingerprintCookie(id, ip, v_loc, v_os, v_browser, v_incog) {
    // console.log(id)
    setCookie(id, ip, v_loc, v_os, v_browser, v_incog);
  }
  if (checkCookie("userFingerPrint") == true) {
    console.log("Cookie Exists");
    console.log(`User Fingerprint: ${getCookie("userFingerPrint")}`)
  }
  else {
    function getVisitorID() {
      const fpPromise = import('https://fpjscdn.net/v3/UnS8qXlX9aVOQncJJVKP')
        .then(FingerprintJS => FingerprintJS.load())
      fpPromise
        .then(fp => fp.get({ extendedResult: true }))
        .then(result => {
          const visitorId = result.visitorId
          const v_IP = result.ip
          const v_location = result.ipLocation.city.name;
          const v_OS = {
            "os": result.os,
            "osVersion": result.osVersion
          }
          const v_Browser = {
            "browser": result.browserName,
            "browserVersion": result.browserVersion
          }
          const v_incognito = result.incognito;
          setDeviceFingerprintCookie(visitorId, v_IP, v_location, v_OS, v_Browser, v_incognito);
          var url = window.location.pathname;
          var filename = url.substring(url.lastIndexOf('/')+1);
          if(filename == "getCustomer"){
            sendDataToSales();
          }
        })
    }
    getVisitorID()
  }