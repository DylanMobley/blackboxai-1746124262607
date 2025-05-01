// frontend/src/services/api.js

import axios from "axios";
import AuthService from "./AuthService";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://localhost:5101"
});

// Auto-attach token to every request
api.interceptors.request.use(config => {
    const token = AuthService.getToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle 401 Unauthorized (optional advanced)
api.interceptors.response.use(
    response => response,
    async error => {
        if (error.response && error.response.status === 401) {
            AuthService.logout();
        }
        return Promise.reject(error);
    }
);

export default api;
