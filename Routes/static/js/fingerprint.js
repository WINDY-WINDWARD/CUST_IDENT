let v_ID;
function userFingerPrint(){
    const fpPromise = import('https://fpjscdn.net/v3/UnS8qXlX9aVOQncJJVKP')
      .then(FingerprintJS => FingerprintJS.load())
    fpPromise
      .then(fp => fp.get())
      .then(result => {
         const visitorId = result.visitorId
         v_ID=visitorId;
    })
}