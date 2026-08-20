// ========================================
// EcoFinds Authentication JavaScript
// ========================================


// ================================
// PASSWORD VISIBILITY
// ================================

function togglePassword(inputId, button) {

    const input = document.getElementById(inputId);

    if (!input) {
        return;
    }


    if (input.type === "password") {

        input.type = "text";

        button.textContent = "🙈";

    } else {

        input.type = "password";

        button.textContent = "👁";

    }

}


// ================================
// ERROR HELPER
// ================================

function showError(inputId, errorId, message) {

    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);


    if (input) {
        input.classList.add("input-error");
    }


    if (error) {
        error.textContent = message;
    }

}


function clearError(inputId, errorId) {

    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);


    if (input) {
        input.classList.remove("input-error");
    }


    if (error) {
        error.textContent = "";
    }

}


// ================================
// LOGIN FORM
// ================================

const loginForm = document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener("submit", function(event) {

        event.preventDefault();


        const email =
            document.getElementById("loginEmail").value.trim();

        const password =
            document.getElementById("loginPassword").value;


        let valid = true;


        clearError(
            "loginEmail",
            "loginEmailError"
        );

        clearError(
            "loginPassword",
            "loginPasswordError"
        );


        // Email validation

        if (email === "") {

            showError(
                "loginEmail",
                "loginEmailError",
                "Please enter your email."
            );

            valid = false;

        } else if (!isValidEmail(email)) {

            showError(
                "loginEmail",
                "loginEmailError",
                "Please enter a valid email address."
            );

            valid = false;

        }


        // Password validation

        if (password === "") {

            showError(
                "loginPassword",
                "loginPasswordError",
                "Please enter your password."
            );

            valid = false;

        }


        if (!valid) {
            return;
        }


        /*
            TEMPORARY FRONTEND BEHAVIOUR

            Later the Flask backend will handle:
            POST /login

            For now we simply show a message.
        */

        showAuthNotification(
            "Login form is valid. Backend will be connected next."
        );

    });

}


// ================================
// SIGNUP FORM
// ================================

const signupForm =
    document.getElementById("signupForm");


if (signupForm) {

    signupForm.addEventListener("submit", function(event) {

        event.preventDefault();


        const name =
            document.getElementById("signupName").value.trim();

        const email =
            document.getElementById("signupEmail").value.trim();

        const password =
            document.getElementById("signupPassword").value;

        const confirmPassword =
            document.getElementById("confirmPassword").value;

        const terms =
            document.getElementById("terms").checked;


        let valid = true;


        // Clear errors

        clearError(
            "signupName",
            "signupNameError"
        );

        clearError(
            "signupEmail",
            "signupEmailError"
        );

        clearError(
            "signupPassword",
            "signupPasswordError"
        );

        clearError(
            "confirmPassword",
            "confirmPasswordError"
        );


        // Name

        if (name === "") {

            showError(
                "signupName",
                "signupNameError",
                "Please enter your full name."
            );

            valid = false;

        } else if (name.length < 2) {

            showError(
                "signupName",
                "signupNameError",
                "Name must contain at least 2 characters."
            );

            valid = false;

        }


        // Email

        if (email === "") {

            showError(
                "signupEmail",
                "signupEmailError",
                "Please enter your email."
            );

            valid = false;

        } else if (!isValidEmail(email)) {

            showError(
                "signupEmail",
                "signupEmailError",
                "Please enter a valid email address."
            );

            valid = false;

        }


        // Password

        if (password === "") {

            showError(
                "signupPassword",
                "signupPasswordError",
                "Please create a password."
            );

            valid = false;

        } else if (password.length < 6) {

            showError(
                "signupPassword",
                "signupPasswordError",
                "Password must contain at least 6 characters."
            );

            valid = false;

        }


        // Confirm password

        if (confirmPassword === "") {

            showError(
                "confirmPassword",
                "confirmPasswordError",
                "Please confirm your password."
            );

            valid = false;

        } else if (password !== confirmPassword) {

            showError(
                "confirmPassword",
                "confirmPasswordError",
                "Passwords do not match."
            );

            valid = false;

        }


        // Terms

        if (!terms) {

            showAuthNotification(
                "Please accept the Terms & Conditions."
            );

            valid = false;

        }


        if (!valid) {
            return;
        }


        /*
            TEMPORARY FRONTEND BEHAVIOUR

            Later Flask will handle:
            POST /signup
        */

        showAuthNotification(
            "Account form is valid. Backend will be connected next."
        );

    });

}


// ================================
// EMAIL VALIDATION
// ================================

function isValidEmail(email) {

    const pattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return pattern.test(email);

}


// ================================
// AUTH NOTIFICATION
// ================================

function showAuthNotification(message) {

    const old =
        document.querySelector(".auth-notification");

    if (old) {
        old.remove();
    }


    const notification =
        document.createElement("div");

    notification.className =
        "auth-notification";

    notification.textContent =
        message;


    notification.style.position = "fixed";
    notification.style.bottom = "25px";
    notification.style.left = "50%";

    notification.style.transform =
        "translateX(-50%)";

    notification.style.zIndex = "9999";

    notification.style.padding =
        "14px 22px";

    notification.style.background =
        "#238b57";

    notification.style.color =
        "#ffffff";

    notification.style.borderRadius =
        "9px";

    notification.style.fontSize =
        "13px";

    notification.style.fontWeight =
        "600";

    notification.style.boxShadow =
        "0 10px 30px rgba(0,0,0,0.15)";


    document.body.appendChild(notification);


    setTimeout(function() {

        notification.style.opacity = "0";

        notification.style.transition =
            "0.3s";

        setTimeout(function() {

            notification.remove();

        }, 300);

    }, 2500);

}