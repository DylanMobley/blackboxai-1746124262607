// frontend/src/components/MicButton.jsx

import React, { useState } from 'react';

const MicButton = ({ onTranscript }) => {
  const [recording, setRecording] = useState(false);
  let mediaRecorder;
  let audioChunks = [];

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.start();
      setRecording(true);

      mediaRecorder.ondataavailable = (e) => {
        audioChunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.wav");

        try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/api/audio`, {
            method: "POST",
            body: formData,
          });
          const data = await response.json();
          console.log("🎤 Audio uploaded:", data.path);

          // OPTIONAL: implement STT (speech-to-text) API here if needed!

          if (onTranscript) {
            onTranscript("Transcription placeholder"); // 🔥 hook to process result later
          }
        } catch (err) {
          console.error("Error uploading audio:", err);
        }

        audioChunks = [];
      };

      setTimeout(() => {
        mediaRecorder.stop();
        setRecording(false);
      }, 5000); // 🎯 Auto-stop after 5 seconds

    } catch (error) {
      console.error("Mic access denied or unavailable.", error);
    }
  };

  return (
    <div>
      <button onClick={startRecording} disabled={recording}>
        {recording ? "🎙️ Recording..." : "🎤 Speak"}
      </button>
    </div>
  );
};

export default MicButton;
