import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import AuthService from "../services/AuthService";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      const response = await api.post("/api/login", {
        email,
        password,
      });

      const token = response.data.token;
      AuthService.saveToken(token);
      navigate("/chat"); // 🧭 redirect to chat or main interface
    } catch (error) {
      const errorText = error.response?.data?.error || "Login failed.";
      setErrorMsg(errorText);
    }
  };

  return (
    <div className="login-container">
      <h2>🔐 Secure Login</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="email"
          placeholder="📧 Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="🔑 Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {errorMsg && <p className="error-message">⚠️ {errorMsg}</p>}

        <button type="submit" className="login-button">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
