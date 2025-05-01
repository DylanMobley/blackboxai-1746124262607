// frontend/src/services/AuthService.js

import api from "./api";

class AuthService {
    static TOKEN_KEY = "mec_auth_token";

    static saveToken(token) {
        localStorage.setItem(this.TOKEN_KEY, token);
    }

    static getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    }

    static removeToken() {
        localStorage.removeItem(this.TOKEN_KEY);
    }

    static isAuthenticated() {
        return !!this.getToken();
    }

    static async login(email, password) {
        const response = await api.post("/api/login", { email, password });
        this.saveToken(response.data.token);
        return response.data;
    }

    static logout() {
        this.removeToken();
        window.location.href = "/login";
    }
}

export default AuthService;
