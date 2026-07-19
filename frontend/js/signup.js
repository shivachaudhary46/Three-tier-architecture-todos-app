import ApiService from "./api.js";

document.addEventListener("DOMContentLoaded", () => {

    const signupForm = document.getElementById("signupform");
    const signupButton = document.getElementById("signupbutton");

    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        signupButton.disabled = true;
        signupButton.textContent = "Creating Account...";

        const bodyData = {
            username: document.getElementById("username").value.trim(), 
            email: document.getElementById("email").value.trim(), 
            password: document.getElementById("password").value
        }

        console.log(bodyData["username"])

        try {
            const response = await fetch(`${ApiService.baseURL}/auth/`, {
                method: "POST", 
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(bodyData)
            });
            const result = await response.json();
            alert("Account created successfully!");
            window.location.href = "login.html";

        } catch (error) {
            alert(error.message || "Registration failed.");
            signupButton.disabled = false;
            signupButton.textContent = "Sign Up";
        }
    });

}); 