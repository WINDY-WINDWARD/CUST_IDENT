let cookieName = "userFingerPrint";
function setCookie(visitorID){
    const d = new Date();
    d.setTime(d.getTime()+(365*24*60*60*1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = `${cookieName} = ${visitorID} ; ${expires}`;
    console.log("Cookie Created");
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
  