// Handling signup form submission
document.getElementById("signup-form").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent default form submission
    
    // Get form data
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Send POST request to the backend
    fetch("http://127.0.0.1:5001/api/auth/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.msg === "User created successfully") {
            alert("Signup successful! You can now log in.");
            window.location.href = "login.html"; // Redirect to login page
        } else {
            alert("Error: " + data.msg);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred, please try again.");
    });
});

// Handling login form submission
document.getElementById("login-form").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent default form submission
    
    // Get form data
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Send POST request to the backend
    fetch("http://127.0.0.1:5001/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token); // Store JWT token in localStorage
            alert("Login successful!");
            window.location.href = "dashboard.html"; // Redirect to user profile page
        } else {
            alert("Error: Invalid credentials");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred, please try again.");
    });
});
