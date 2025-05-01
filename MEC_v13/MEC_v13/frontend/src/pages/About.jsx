// frontend/src/pages/About.jsx

import React from "react";
import "./About.css"; // (optional styling if you want)

const About = () => {
    return (
        <div className="about-container">
            <h1>🧠 About MEC_v13+</h1>

            <section className="about-section">
                <h2>🎯 Purpose</h2>
                <p>
                    MEC_v13+ is a full-production emotional intelligence middleware system designed to enable real-time,
                    emotionally resonant, and agentic AI interactions. It combines symbolic reasoning, neural LLMs,
                    emotional ontologies (EIL/ESIL), multimodal emotion processing, and clone-based TTS animation technologies.
                </p>
            </section>

            <section className="about-section">
                <h2>🔥 Key Features</h2>
                <ul>
                    <li>Emotionally Intelligent Conversations via deep EIL/ESIL parsing.</li>
                    <li>Dynamic Symbolic Reasoning using upgraded AtomSpace + MetaRules.</li>
                    <li>Persona Management System with hot-swappable personalities.</li>
                    <li>Empathy-Driven LLM Fusion for rich emotional context generation.</li>
                    <li>Real-time Voice Cloning & Avatar Animation with Bark and SadTalker.</li>
                    <li>Front-end AI Agent Interface with webcam, mic, graph visualization.</li>
                    <li>Full Production Hardening: CORS, RBAC, JWT Auth, Rate Limits, Logging, Grafana metrics.</li>
                    <li>Fully Dockerized Microservices Architecture for easy scaling.</li>
                    <li>Model Hot-Swapping and Async Expansion ready.</li>
                </ul>
            </section>
        </div>
    );
};

export default About;
