let products = document.querySelectorAll('.product');
let prodID;
let prodName;
products.forEach(item =>{
    item.addEventListener("click",()=>{
        // console.log("Clicked");
        prodID=item.id;
        prodName=item.getAttribute("name");
        window.sessionStorage.setItem("productID",prodID);
        window.sessionStorage.setItem("productName",prodName);
        window.location.href = "/product";
    })
})