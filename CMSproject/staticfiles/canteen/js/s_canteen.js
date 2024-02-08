const aside = document.getElementsByClassName("aside")[0];
const main = document.getElementsByClassName("main")[0];
const navbarHeight = document.getElementsByClassName("navbar")[0].clientHeight;
const windowHeight = window.innerHeight;
const profileOptions = document.getElementsByClassName("profileOptions")[0];

function adjustHeight(){
    aside.style.height = (windowHeight - navbarHeight) + 'px';
    main.style.height = (windowHeight - navbarHeight) + 'px';
    main.style.maxHeight = (windowHeight - navbarHeight) + 'px';

}
adjustHeight();

function showProfileOptions(){
    if (profileOptions.style.display === '' || profileOptions.style.display === 'none'){
        profileOptions.style.display = 'block';
    }
    else{
        profileOptions.style.display = 'none';
    }
}
 var box = document.getElementById('batta');
 var down = false;
 function togglenoti()
 {
    if(down){
       box.style.height = '0px';
       box.style.opacity = 0;
       down = false; 
    }
    else{
        box.style.opacity=1;
        down = true;
        box.style.height = '400px';

    }
 }
 function addItem() {
    // Get values from input fields
    var itemName = document.getElementById("itemName").value;
    var itemPrice = document.getElementById("itemPrice").value;
    var itemImageInput = document.getElementById("itemImageInput");

    // Check if a file is selected
    if (itemImageInput.files.length > 0) {
        var itemImage = URL.createObjectURL(itemImageInput.files[0]);

        // Create a new item div
        var newItem = document.createElement("div");
        newItem.className = "item";
        newItem.innerHTML = `
            <img src="${itemImage}" alt="${itemName}">
            <div class="itemName">${itemName}</div>
            <div class="itemPrice"> Rs. ${itemPrice} /- </div>
            <button onclick="deleteItem(this)">Delete Item</button>
        `;

        // Append the new item to the menu container
        document.getElementById("menuItemsContainer").appendChild(newItem);

        // Clear input fields after adding the item
        document.getElementById("itemName").value = "";
        document.getElementById("itemPrice").value = "";
        itemImageInput.value = ""; // Clear the file input
    } else {
        alert("Please select an image for the item.");
    }
}
function AddToSpecial(button) {
    // Get the parent div of the item
    var itemDiv = button.parentNode;

    // Retrieve item details
    var itemName = itemDiv.querySelector(".itemName").textContent;
    var itemPrice = itemDiv.querySelector(".itemPrice").textContent;
    var itemImageSrc = itemDiv.querySelector("img").src;

    // Create a new item div
    var newItem = document.createElement("div");
    newItem.classList.add("item");
    newItem.innerHTML = `
        <img src="${itemImageSrc}" alt="${itemName}">
        <div class="itemName">${itemName}</div>
        <div class="itemPrice">${itemPrice}</div>
        <button onclick="deleteItem(this)">Delete Item</button>
    `;

    // Append the new item to the menuItemsContainer
    var menuItemsContainer = document.getElementById("menuItemsContainer");
    menuItemsContainer.appendChild(newItem);
    button.textContent = "Added!";

}

function deleteItem(button) {
    // Get the parent element (item) of the clicked button
    var item = button.parentNode;

    // Remove the item from the DOM
    item.parentNode.removeChild(item);
}

function orderItem(button) {
    // Add your ordering logic here
    // You can access the item details using the button's parent elements
    var itemName = button.parentNode.querySelector(".itemName").innerText;
    var itemPrice = button.parentNode.querySelector(".itemPrice").innerText;

    // Add your ordering logic here, for example, display an alert
    alert(`Ordered ${itemName} for ${itemPrice}`);
} 
function addItems() {
    // Get values from input fields
    var itemsName = document.getElementById("itemsName").value;
    var itemsPrice = document.getElementById("itemsPrice").value;
    var itemsImageInput = document.getElementById("itemsImageInput");

    // Check if a file is selected
    if (itemsImageInput.files.length > 0) {
        var itemsImage = URL.createObjectURL(itemsImageInput.files[0]);

        // Create a new item div
        var newItems = document.createElement("div");
        newItems.className = "item";
        newItems.innerHTML = `
            <img src="${itemsImage}" alt="${itemsName}">
            <div class="itemsName">${itemsName}</div>
            <div class="itemsPrice"> Rs. ${itemsPrice} /- </div>
            <button onclick="deleteItem(this)">Delete Item</button>
        `;

        // Append the new item to the menu container
        document.getElementById("menus").appendChild(newItems);

        // Clear input fields after adding the item
        document.getElementById("itemsName").value = "";
        document.getElementById("itemsPrice").value = "";
        itemsImageInput.value = ""; // Clear the file input
    } else {
        alert("Please select an image for the item.");
    }
}
