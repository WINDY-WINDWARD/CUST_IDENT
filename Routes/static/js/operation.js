let categories = document.querySelectorAll('.category');
categories.forEach(item =>{
    item.addEventListener("click",()=>{
        window.sessionStorage.setItem("categoryID",item.id);
        window.location.href = "/bangles";
    })
})