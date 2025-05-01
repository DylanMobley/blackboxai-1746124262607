// frontend/src/components/TTSPlayback.jsx

import React, { useEffect, useState } from 'react';

const TTSPlayback = ({ text }) => {
  const [audioUrl, setAudioUrl] = useState(null);

  useEffect(() => {
    if (!text) return;

    const fetchAudio = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_TTS_API_URL}/tts/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });

        const data = await response.json();
        if (data.audio_url) {
          const fullUrl = `${import.meta.env.VITE_TTS_API_URL}${data.audio_url}`;
          setAudioUrl(fullUrl);

          const audio = new Audio(fullUrl);
          audio.play();
        }
      } catch (error) {
        console.error("TTS playback error:", error);
      }
    };

    fetchAudio();
  }, [text]); // 🧠 Fetch new audio every time bot sends new text!

  return null; // No manual button needed for auto-play
};

export default TTSPlayback;
