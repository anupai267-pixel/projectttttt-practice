// ================================
// EcoFinds - Main JavaScript
// ================================


// Mobile navigation
const menuBtn = document.getElementById("menuBtn");
const navLinks = document.getElementById("navLinks");

if (menuBtn && navLinks) {

    menuBtn.addEventListener("click", function () {

        navLinks.classList.toggle("show");

        if (navLinks.classList.contains("show")) {
            menuBtn.textContent = "✕";
        } else {
            menuBtn.textContent = "☰";
        }

    });

}


// Wishlist button
function toggleWishlist(button) {

    button.classList.toggle("active");

    if (button.classList.contains("active")) {

        button.textContent = "♥";

        showNotification("Added to wishlist!");

    } else {

        button.textContent = "♡";

        showNotification("Removed from wishlist.");

    }

}


// Search
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

if (searchForm) {

    searchForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const searchValue = searchInput.value.trim();

        if (searchValue === "") {

            showNotification("Please enter something to search.");

            return;
        }

        // Temporary frontend behavior.
        // Backend search will be connected later.
        window.location.href =
            "products.html?search=" +
            encodeURIComponent(searchValue);

    });

}


// Notification
function showNotification(message) {

    const oldNotification =
        document.querySelector(".eco-notification");

    if (oldNotification) {
        oldNotification.remove();
    }


    const notification =
        document.createElement("div");

    notification.className =
        "eco-notification";

    notification.textContent =
        message;


    notification.style.position = "fixed";
    notification.style.bottom = "25px";
    notification.style.right = "25px";
    notification.style.zIndex = "9999";

    notification.style.padding = "14px 20px";

    notification.style.background = "#238b57";
    notification.style.color = "#ffffff";

    notification.style.borderRadius = "9px";

    notification.style.fontSize = "14px";
    notification.style.fontWeight = "600";

    notification.style.boxShadow =
        "0 10px 30px rgba(0,0,0,0.15)";


    document.body.appendChild(notification);


    setTimeout(function () {

        notification.style.opacity = "0";
        notification.style.transition = "0.3s";

        setTimeout(function () {
            notification.remove();
        }, 300);

    }, 2000);

}