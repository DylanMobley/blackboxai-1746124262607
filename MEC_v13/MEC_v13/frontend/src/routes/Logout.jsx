// frontend/src/routes/Logout.jsx

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/AuthService";

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    AuthService.removeToken();
    navigate("/login");
  }, [navigate]);

  return null;
};

export default Logout;
