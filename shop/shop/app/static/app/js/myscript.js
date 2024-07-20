document.addEventListener('DOMContentLoaded', function() {
    // Selecting DOM elements for slider functionality
    let leftbtn = document.querySelector(".btn-l");
    let rightbtn = document.querySelector(".btn-r");
    let slider = document.querySelector(".slider-sec");

    rightbtn.addEventListener('click', function(event) {
        let c = document.querySelector(".product-slide");
        c.scrollLeft += 1100;
        event.preventDefault();
    });

    leftbtn.addEventListener('click', function(event) {
        let c = document.querySelector(".product-slide");
        c.scrollLeft -= 1100;
        event.preventDefault();
    });

    // Selecting DOM elements for login functionality
    const loginBtn = document.querySelector('.login-btn');
    const loginForm = document.querySelector('.login-form');
    const backArrow = document.querySelector('.fa-arrow-left');

    // Adding event listener for loginBtn click
    if (loginBtn) {
        loginBtn.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission
            // Toggle the display of loginForm
            if (loginForm.style.display === 'none' || loginForm.style.display === '') {
                loginForm.style.display = 'block';
            } else {
                loginForm.style.display = 'none';
            }
        });
    }

    // Adding event listener for backArrow click
    if (backArrow) {
        backArrow.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior
            loginForm.style.display = 'none'; // Hide loginForm
        });
    }

    // Selecting DOM elements for account box functionality
    const accountBtn = document.querySelector('.account_btn');
    const accountBox = document.querySelector('.account_box');

    // Adding event listener for accountBtn click
    if (accountBtn) {
        accountBtn.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default behavior
            // Toggle the display of accountBox
            if (accountBox.style.display === 'none' || accountBox.style.display === '') {
                accountBox.style.display = 'block';
            } else {
                accountBox.style.display = 'none';
            }
        });
    }
});
