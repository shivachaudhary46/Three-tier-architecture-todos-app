import ApiService from "./api.js";

document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginform");
    const loginButton = document.getElementById("loginButton");

    loginForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;

        try {
            const response = await ApiService.login({
                username,
                password,
            });

            const user = await ApiService.getCurrentUser();

            localStorage.setItem(
                "userData",
                JSON.stringify(user)
            );

            window.location.href = "todos.html";

        } catch (error) {

            alert(error.message);

            loginButton.disabled = false;
            loginButton.textContent = "Sign In";
        }
    });

});