const API_BASE_URL = "http://127.0.0.1:8000";

class ApiService {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.token = localStorage.getItem('authToken');
    }

    async request(endpoint, options = {}) {

        const headers = {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        };

        if (this.token) {
            headers["Authorization"] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                ...options,
                headers,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Request failed");
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }

    }

    async login(credentials) {
        const formData = new URLSearchParams();
        formData.append("username", credentials.username);
        formData.append("password", credentials.password);

        try {
            const response = await fetch(`${this.baseURL}/auth/token`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Invalid username or password");
            }

            if (data.access_token) {
                this.token = data.access_token;
                localStorage.setItem("authToken", data.access_token);
            }

            return data;
        } catch (error) {
            console.error('Login Error:', error);
            throw error;
        }
    } 

    async getCurrentUser() {
        return this.request("/auth/me");
    }

    logout() {
        this.token = null; 
        localStorage.clear();
        window.location.href = "login.html";
    }

    async checkAuth() {
        this.token = localStorage.getItem("authToken");

        if (!this.token) {
            window.location.href = "/login.html";
            return false;
        }

        try {
            const res = await this.getCurrentUser();
            return true; 
        } catch {
            window.location.href = "/login.html";
            return false;
        }
    }

    async getNotes() {
        return this.request("/todos/notes", {
            method: "GET",
        });
    }

    async createNote(title) {
        return this.request("/todos/notes", {
            method: "POST",
            body: JSON.stringify({
                title: title,
            }),
        });
    }

    async updateNote(id, title) {
        return this.request("/todos/update", {
            method: "PUT",
            body: JSON.stringify({
                id: id,
                title: title,
            }),
        });
    }

    async deleteNote(id) {
        return this.request("/todos/delete", {
            method: "DELETE",
            body: JSON.stringify({
                id: id,
            }),
        });
    }
}

export default new ApiService();