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
