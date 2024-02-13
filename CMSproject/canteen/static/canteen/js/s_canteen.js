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

toastr.options = {
    progressBar: true,
    positionClass: 'toast-bottom-right',
    preventDuplicates: false,
    onclick: null,
};

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

function addmenuItem() {
    // Get values from input fields
    var itemName = document.getElementById("itemsName").value;
    var itemPrice = document.getElementById("itemsPrice").value;
    var itemDescription = document.getElementById("itemsDescription").value;
    var itemImageInput = document.getElementById("itemsImageInput");

    // Check if a file is selected
    if (itemImageInput.files.length > 0) {
        var itemImage = URL.createObjectURL(itemImageInput.files[0]);
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Prepare the data for the fetch request
        var formData = new FormData();
        formData.append('itemsName', itemName);
        formData.append('itemsPrice', itemPrice);
        formData.append('itemsDescription', itemDescription);
        formData.append('itemsImageInput', itemImageInput.files[0]);
        var url = document.querySelector('button[data-url]').dataset.url;
        // Send the data to the server using fetch
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log('success vayo hai data base ma halney kaam');
            // Access the details of the newly added item directly from data
            var newItem = document.createElement("div");
            newItem.className = "item";
            newItem.innerHTML = `
                <img src="${itemImage}" alt="${itemName}">
                <div class="itemName">${itemName}</div>
                <div class="item.description">${data.item.description}</div>
                <div class="itemPrice"> Rs. ${itemPrice} /- </div>
                <button onclick="deleteItem(this)">Delete Item</button>
                <button onclick="AddToSpecial(this)">Add to Specials</button>
            `;
            console.log('aba naya div banaudaii to display the added menu');
            // Append the new item to the menu container
            document.getElementById("menus").appendChild(newItem);
            // Clear input fields after adding the item
            document.getElementById("itemsName").value = "";
            document.getElementById("itemsPrice").value = "";
            document.getElementById("itemsDescription").value = "";
            itemsImageInput.value = ""; // Clear the file input
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
    toastr.success(`${itemName} is added to special!`);

}

function deleteItem(button) {
    var item = button.parentNode;
    var itemName = item.querySelector(".itemName").textContent;

    // remove the item
    item.parentNode.removeChild(item);
    toastr.success(`${itemName} is deleted!`);
}



