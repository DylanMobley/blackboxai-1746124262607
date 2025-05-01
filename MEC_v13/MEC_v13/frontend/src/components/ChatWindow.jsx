// frontend/src/components/ChatWindow.jsx

import React, { useState, useEffect } from "react";
import api from "../services/api";
import AuthService from "../services/AuthService";
import "../App.css";

const ChatWindow = () => {
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState("");
    const [persona, setPersona] = useState("soothing_ally");
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!AuthService.isAuthenticated()) {
            alert("🛡️ You must log in first.");
            return;
        }

        if (!userInput.trim()) return;

        const newMessage = { sender: "user", text: userInput };
        setMessages(prev => [...prev, newMessage]);
        setUserInput("");
        setLoading(true);

        try {
            const response = await api.post("/api/message", {
                user_input: userInput,
                persona: persona
            });

            const botReply = { sender: "agent", text: response.data.response };
            setMessages(prev => [...prev, botReply]);
        } catch (error) {
            console.error("🚨 Send failed:", error);
            setMessages(prev => [...prev, { sender: "error", text: "⚠️ Message failed to send." }]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="chat-window">
            <div className="chat-messages">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`chat-message ${msg.sender}`}
                    >
                        {msg.text}
                    </div>
                ))}
            </div>

            <div className="chat-input">
                <textarea
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type a message..."
                />
                <button onClick={sendMessage} disabled={loading}>
                    {loading ? "Sending..." : "Send"}
                </button>
            </div>
        </div>
    );
};

export default ChatWindow;
