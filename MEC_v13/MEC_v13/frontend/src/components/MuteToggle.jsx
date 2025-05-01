// frontend/src/components/MuteToggle.jsx

import React, { useState, useEffect } from 'react';

const MuteToggle = () => {
  const [muted, setMuted] = useState(localStorage.getItem("tts_muted") === "true");

  const toggleMute = () => {
    const newState = !muted;
    setMuted(newState);
    localStorage.setItem("tts_muted", newState.toString());
  };

  useEffect(() => {
    const savedState = localStorage.getItem("tts_muted") === "true";
    setMuted(savedState);
  }, []);

  return (
    <button onClick={toggleMute}>
      {muted ? "🔇 TTS Muted" : "🔊 TTS Active"}
    </button>
  );
};

export default MuteToggle;
