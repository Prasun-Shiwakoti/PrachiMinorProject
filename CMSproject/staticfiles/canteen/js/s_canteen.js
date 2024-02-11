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

document.addEventListener('DOMContentLoaded', function () {
    // Fetch menu items from the server
    fetch('{% url "get_menu_items" %}')
        .then(response => response.json())
        .then(data => {
            // Access the menu items array
            var menuItems = data.menu_items;

            // Render menu items dynamically
            var menuContainer = document.getElementById('menus');
            menuContainer.innerHTML = '';  // Clear existing items

            menuItems.forEach(item => {
                var newItem = document.createElement('div');
                newItem.className = 'item';
                newItem.innerHTML = `
                    <img src="${item.image_url}" alt="${item.name}">
                    <div class="itemName">${item.name}</div>
                    <div class="itemPrice"> Rs. ${item.price} /- </div>
                    <button onclick="deleteItem(this)">Delete Item</button>
                `;
                menuContainer.appendChild(newItem);
            });
        })
        .catch(error => {
            console.error('Error fetching menu items:', error);
        });
});


function addmenuItem() {
    // Get values from input fields
    var itemName = document.getElementById("itemName").value;
    var itemPrice = document.getElementById("itemPrice").value;
    var itemImageInput = document.getElementById("itemImageInput").files[0];

    // Check if a file is selected
    if (itemImageInput.files.length > 0) {
        var itemImage = URL.createObjectURL(itemImageInput.files[0]);

        // Prepare the data for the fetch request
        var formData = new FormData();
        formData.append('itemsName', itemName);
        formData.append('itemsPrice', itemPrice);
        formData.append('itemsImageInput', itemImageInput.files[0]);
        var url = document.querySelector('button[data-url]').dataset.url;
        // Send the data to the server using fetch
        fetch(url, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log('success vayo hai data base ma halney kaam')
             // Access the details of the newly added item
             var newItemDetails = data.item;
            var newItem = document.createElement("div");
            newItem.className = "item";
            newItem.innerHTML = `
                <img src="${itemImage}" alt="${itemName}">
                <div class="itemName">${itemName}</div>
                <div class="itemPrice"> Rs. ${itemPrice} /- </div>
                <button onclick="deleteItem(this)">Delete Item</button>
            `;
            console.log('aba naya div banaudaii to display the added menu');
            // Add new item to the menu container
            document.getElementById("menuItemsContainer").appendChild(newItem);

            // Clear input fields after adding the item
            document.getElementById("itemName").value = "";
            document.getElementById("itemPrice").value = "";
            itemImageInput.value = ""; // Clear the file input
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        toastr.error('Please select an image for the item.');
    }
}
function AddToSpecial(button) {
    var itemDiv = button.parentNode;

    // get item details
    var itemName = itemDiv.querySelector(".itemName").textContent;
    var itemPrice = itemDiv.querySelector(".itemPrice").textContent;
    var itemImageSrc = itemDiv.querySelector("img").src;

    // create new div
    var newItem = document.createElement("div");
    newItem.classList.add("item");
    newItem.innerHTML = `
        <img src="${itemImageSrc}" alt="${itemName}">
        <div class="itemName">${itemName}</div>
        <div class="itemPrice">${itemPrice}</div>
        <button onclick="deleteItem(this)">Delete Item</button>
    `;

    // add new item to the menuItemsContainer
    var menuItemsContainer = document.getElementById("menuItemsContainer");
    menuItemsContainer.appendChild(newItem);
    button.textContent = "Added!";

}

function deleteItem(button) {
    var item = button.parentNode;

    // remove the item
    item.parentNode.removeChild(item);
}

function orderItem(button) {
    // add your ordering logic here
    var itemName = button.parentNode.querySelector(".itemName").innerText;
    var itemPrice = button.parentNode.querySelector(".itemPrice").innerText;

    toastr.success(`Ordered ${itemName} for ${itemPrice}`, 'Order Placed');
} 

