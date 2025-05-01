// frontend/src/App.jsx

import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import ChatWindow from "./components/ChatWindow";
import AgentAvatar from "./components/AgentAvatar";
import TTSPlayback from "./components/TTSPlayback";
import PersonaSwitcher from "./components/PersonaSwitcher";
import DiagnosticPanel from "./components/DiagnosticPanel";

import Login from "./routes/Login";
import AboutPage from "./routes/AboutPage";
import ProtectedRoute from "./routes/ProtectedRoute";

import "./App.css";

const App = () => {
  const [persona, setPersona] = useState("soothing_ally");
  const [lastAIResponse, setLastAIResponse] = useState("");

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/about" element={<AboutPage />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <div className="container">
                <div className="agent-panel">
                  <AgentAvatar persona={persona} />
                  <PersonaSwitcher persona={persona} setPersona={setPersona} />
                  <ChatWindow onReply={setLastAIResponse} persona={persona} />
                  <TTSPlayback text={lastAIResponse} />
                  <DiagnosticPanel />
                </div>
              </div>
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;
