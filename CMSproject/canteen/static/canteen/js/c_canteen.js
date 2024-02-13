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
        // box.style.width = '220px';
    }
 }
 var currentItem = null; // To store the reference to the currently selected item

 function openQuantityPopup(button) {
    currentItem = button.parentNode; // Store the reference to the clicked button's parent (item) for later use
    var quantityPopup = currentItem.querySelector('.quantity-popup');

    // Show the quantity popup
    quantityPopup.style.display = "block";
    quantityPopup.style.top = button.offsetTop + button.offsetHeight + 'px';
    quantityPopup.style.left = button.offsetLeft + 'px';
}

    function orderItem() {
        // Get the quantity from the input field
        var quantity = document.getElementById("quantityInput").value;

        // Check if the quantity is valid
        if (!isNaN(quantity) && parseInt(quantity) > 0) {
            toastr.success("You ordered " + quantity + " " + currentItem.querySelector('.itemName').innerText + "(s).");
            // You can handle the order logic here

            // Hide the quantity popup
            closePopup();
        } else {
           toastr.error('Please ender a valid quantity.');
        }
    }
    function closePopup(){
        var quantityPopup = currentItem.querySelector('.quantity-popup');
        quantityPopup.style.display = "none";
    }