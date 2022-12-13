//Cookie Master Functions
let cookieName = "userFingerPrint";
function setCookie(visitorID,User_IP,v_Location,v_OS,v_Browser,v_incognito,catID,pID){
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
    window.sessionStorage.setItem("productID",pID);
    displayDetails(catID, pID, visitorID);
}
function checkCookie(name){
  if(getCookie(name).length()<=0){
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
function checkCookie() {
    var user = getCookie(cookieName);
    // checking whether user is null or not
    if (user != "") {
      return true;
    }
    //if user is null
    else {
    //   setCookie();
      return false;
    }
  }


  //

  function displayDetails(catID,pID,u_ID){
    $.ajax({
        url: '/getCustomer/setUserData',
        type: "POST",
        data: JSON.stringify(
          {"_id": `${u_ID}`,
           "data": {
                "CatgoryID": `${catID}`,
                "ProductID":`${pID}`
            },
            "timestamp": `${Date.now()}`
          }
          ),
        dataType: "json",
        contentType: "application/json",
        });  
}