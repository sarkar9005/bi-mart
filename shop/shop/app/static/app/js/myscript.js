document.addEventListener('DOMContentLoaded', function () {
    // Slider buttons functionality
    let leftbtn = document.querySelector(".btn-l");
    let rightbtn = document.querySelector(".btn-r");
    let slider = document.querySelector(".slider-sec");

    if (rightbtn) {
        rightbtn.addEventListener('click', function (event) {
            let c = document.querySelector(".product-slide");
            c.scrollLeft += 1100;
            event.preventDefault();
        });
    }

    if (leftbtn) {
        leftbtn.addEventListener('click', function (event) {
            let c = document.querySelector(".product-slide");
            c.scrollLeft -= 1100;
            event.preventDefault();
        });
    }

    // Account box functionality
    const accountBtn = document.querySelector('.account_btn');
    const accountBox = document.querySelector('.account_box');

    if (accountBtn) {
        accountBtn.addEventListener('click', function (event) {
            event.preventDefault();
            accountBox.style.display = (accountBox.style.display === 'none' || accountBox.style.display === '') ? 'block' : 'none';
        });
    }

    // Hide cart notification if total count is zero
    const cartNotification = document.querySelector('.cart-button');
    if (cartNotification) {
        const totalCount = parseInt(cartNotification.querySelector('.total-count').innerText.split(' ')[0], 10);
        cartNotification.style.display = (totalCount === 0) ? 'none' : 'block';
    }

    // Popup functionality
    let continueButton = document.querySelector('.continue_loig');
    let popupOverlay = document.querySelector('.popup-overlay');
    let closePopup = document.querySelector('.close-popup');

    if (continueButton && popupOverlay) {
        continueButton.addEventListener('click', function () {
            popupOverlay.style.display = 'flex'; // Show the popup
        });
    }

    if (closePopup && popupOverlay) {
        closePopup.addEventListener('click', function () {
            popupOverlay.style.display = 'none'; // Hide the popup
        });
    }

    if (popupOverlay) {
        popupOverlay.addEventListener('click', function (event) {
            if (event.target === popupOverlay) {
                popupOverlay.style.display = 'none'; // Hide the popup
            }
        });
    }

    // Trigger and close popup
    var trigger = document.getElementById('popup-trigger');
    var popup = document.getElementById('popup');
    var close = popup ? popup.querySelector('.close') : null;

    if (trigger) {
        trigger.addEventListener('click', function (event) {
            event.preventDefault();
            if (popup) {
                popup.style.display = 'block';
            }
        });
    }

    if (close) {
        close.addEventListener('click', function () {
            if (popup) {
                popup.style.display = 'none';
            }
        });
    }

    // Close the popup when clicking outside of it
    window.addEventListener('click', function (event) {
        if (popup && event.target === popup) {
            popup.style.display = 'none';
        }
    });

    // Close the popup if 'Escape' key is pressed
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            if (popup) {
                popup.style.display = 'none';
            }
        }
    });

    // Cart popup functionality
    function openCartPopup() {
        const cartPopup = document.getElementById('cart-popup');
        const overlay = document.getElementById('overlay');
        cartPopup.style.display = 'block';  // Show cart popup
        overlay.style.display = 'block';    // Show overlay
        overlay.classList.add('show');      // Add 'show' class to overlay
        document.body.classList.add('fixed-position');  // Fix the background
    }

    function closeCartPopup() {
        const cartPopup = document.getElementById('cart-popup');
        const overlay = document.getElementById('overlay');
        cartPopup.style.display = 'none';   // Hide cart popup
        overlay.style.display = 'none';     // Hide overlay
        overlay.classList.remove('show');   // Remove 'show' class from overlay
        document.body.classList.remove('fixed-position');  // Unfix the background
    }

    document.getElementById('open-cart-btn').onclick = function() {
        openCartPopup();
    }

    document.getElementById('close-cart-btn').onclick = function() {
        closeCartPopup();
    }

    window.onclick = function(event) {
        const cartPopup = document.getElementById('cart-popup');
        const overlay = document.getElementById('overlay');
        if (event.target === overlay) {
            closeCartPopup();
        }
    }

    // Hide or show mobile_cart based on the total count
    function updateMobileCartVisibility() {
        const mobileCart = document.querySelector('.mobile_cart');
        const totalCountElement = document.querySelector('.cart-button .total-count');
        if (totalCountElement) {
            const totalCount = parseInt(totalCountElement.innerText.split(' ')[0], 10);
            mobileCart.style.display = (totalCount === 0) ? 'none' : 'block';
        }
    }

    // Initial visibility
    updateMobileCartVisibility();

    // Update visibility when cart count changes
    const observer = new MutationObserver(updateMobileCartVisibility);
    const totalCountElement = document.querySelector('.cart-button .total-count');
    if (totalCountElement) {
        observer.observe(totalCountElement, { childList: true, subtree: true });
    }

    // Add product to cart example function
    function addProductToCart() {
        // Your existing logic to add product to cart...
        updateMobileCartVisibility();
    }

    // Example function call to add product to cart
    const addToCartButton = document.querySelector('#add-to-cart-button');
    if (addToCartButton) {
        addToCartButton.addEventListener('click', addProductToCart);
    }
});

 // Cart popup functionality
 function openCartPopup() {
    const cartPopup = document.getElementById('cart-popup');
    const overlay = document.getElementById('overlay');
    cartPopup.style.display = 'block';  // Show cart popup
    overlay.style.display = 'block';    // Show overlay
}

function closeCartPopup() {
    const cartPopup = document.getElementById('cart-popup');
    const overlay = document.getElementById('overlay');
    cartPopup.style.display = 'none';   // Hide cart popup
    overlay.style.display = 'none';     // Hide overlay
}

document.getElementById('open-cart-btn').onclick = function() {
    openCartPopup();
}

document.getElementById('close-cart-btn').onclick = function() {
    closeCartPopup();
}

window.onclick = function(event) {
    const cartPopup = document.getElementById('cart-popup');
    const overlay = document.getElementById('overlay');
    if (event.target === overlay) {
        closeCartPopup();
    }
}

// Hide or show mobile_cart based on the total count
function updateMobileCartVisibility() {
    const mobileCart = document.querySelector('.mobile_cart');
    const totalCountElement = document.querySelector('.cart-button .total-count');
    if (totalCountElement) {
        const totalCount = parseInt(totalCountElement.innerText.split(' ')[0], 10);
        mobileCart.style.display = (totalCount === 0) ? 'none' : 'block';
    }
}

// Initial visibility
updateMobileCartVisibility();

// Update visibility when cart count changes
const observer = new MutationObserver(updateMobileCartVisibility);
const totalCountElement = document.querySelector('.cart-button .total-count');
if (totalCountElement) {
    observer.observe(totalCountElement, { childList: true, subtree: true });
}

// Add product to cart with error handling
function addProductToCart1(str, quantity, remove)
{
    
    $.ajax({
        type: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
        },
        url:'/add-to-cart/',
        datatype: 'json',
        data: JSON.stringify({
            product_id: str,
            quantity: quantity,
            remove: remove,
        }),
        success: function (response) {
            console.log(response);
            if(response.success == true ){
                
                if(response.error_status == "true")
                {
                    $("#notifiaction_error").html(response.error);
                }
                
                if(response.quantity > 0)
                {
                    $(".product_button_"+str).show();
                    $(".product_add_button_"+str).hide();
                    $(".prod_quantity_"+str).show();
                }
                else{
                    $(".product_add_button_"+str).show();
                    $(".product_button_"+str).hide();
                    $(".prod_quantity_"+str).hide();    
                    
                }

                $(".prod_que_"+str).html(response.quantity);
                $(".total_items").html(response.total_count);
                $(".total_cost").html(response.totalsum);
                var grand_cost = response.totalsum;    
                if(grand_cost > 200)
                {
                    $(".grand_cost").html(grand_cost);
                }
                else{
                    grand_cost = grand_cost + 16;
                    $(".grand_cost").html(grand_cost);
                }  


            }else{
                $("#notifiaction_error").html(response.error);                
                $("#notifiaction_error").fadeIn("slow");   
                $("#notifiaction_error").delay(2000).fadeOut("slow");   
               
            }
            
        }
    });
}

function addProductToCart(productId, quantity, remove = false) {
    fetch('/add_to_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
            remove: remove
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showPopupMessage(data.error);
        } else {
            // Update cart visibility and count
            updateMobileCartVisibility();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Example function call to add product to cart
const addToCartButton = document.querySelector('#add-to-cart-button');
if (addToCartButton) {
    addToCartButton.addEventListener('click', function() {
        const productId = addToCartButton.dataset.productId;
        const quantity = 1; // Example quantity
        addProductToCart(productId, quantity);
    });
}

// Show a popup message
function showPopupMessage(message) {
    const popupOverlay = document.getElementById('popup-overlay');
    const popupMessage = document.getElementById('popup-message');
    popupMessage.innerText = message;
    popupOverlay.style.display = 'block';
}

// Hide the popup message
function hidePopupMessage() {
    const popupOverlay = document.getElementById('popup-overlay');
    popupOverlay.style.display = 'none';
}

document.getElementById('popup-overlay').addEventListener('click', function (event) {
    if (event.target === this || event.target.classList.contains('close-popup')) {
        hidePopupMessage();
    }
});

// Check stock availability
function checkStockAvailability() {
    document.querySelectorAll('.cart-section').forEach(function (section) {
        const productId = section.getAttribute('data-product-id');
        fetch(`/check_stock/${productId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.in_stock === false) {
                    section.querySelector('.add-to-cart-btn').disabled = true;
                    section.querySelector('.add-to-cart-btn').innerText = 'Out of Stock';
                    showPopupMessage('The product is out of stock.');
                }
            });
    });
}



document.addEventListener('DOMContentLoaded', function () {
    // Function to update cart UI
    function updateCartUI(data) {
        if (data.success) {
            // Update cart count
            document.querySelector('.total-count').innerText = `${data.total_count} items`;

            // Show mobile cart if items are present
            updateMobileCartVisibility();
        } else if (data.error) {
            alert(data.error);
        }
    }

    // AJAX request to add product to cart
    function addProductToCart(productId, quantity, remove = false) {
        fetch('/add_to_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest' // Indicate that this is an AJAX request
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity,
                remove: remove
            })
        })
        .then(response => response.json())
        .then(data => updateCartUI(data))
        .catch(error => console.error('Error:', error));
    }

    // Event listener for Add to Cart button
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const productId = this.querySelector('[name="product_id"]').value;
            addProductToCart(productId, 1); // Default quantity 1
        });
    });

    // Function to update the visibility of the mobile cart button
    function updateMobileCartVisibility() {
        const mobileCart = document.querySelector('.mobile_cart');
        const totalCountElement = document.querySelector('.total-count');
        if (totalCountElement) {
            const totalCount = parseInt(totalCountElement.innerText.split(' ')[0], 10);
            mobileCart.style.display = (totalCount > 0) ? 'block' : 'none';
        }
    }

    // Initial call to update mobile cart visibility
    updateMobileCartVisibility();

    // Observe changes to total count to update mobile cart visibility
    const observer = new MutationObserver(updateMobileCartVisibility);
    const totalCountElement = document.querySelector('.total-count');
    if (totalCountElement) {
        observer.observe(totalCountElement, { childList: true, subtree: true });
    }
});

// Utility function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
