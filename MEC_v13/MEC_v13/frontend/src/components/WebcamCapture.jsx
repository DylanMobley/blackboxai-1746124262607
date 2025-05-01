import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';

const WebcamCapture = () => {
  const webcamRef = useRef(null);
  const [feedback, setFeedback] = useState("");

  const captureAndSend = async () => {
    const screenshot = webcamRef.current.getScreenshot();

    if (!screenshot) {
      setFeedback("📷 No image captured.");
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/webcam', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_base64: screenshot })
      });

      const result = await response.json();
      setFeedback(`🧠 AI Insight: ${result.emotion || "unknown"}`);
    } catch (err) {
      console.error("Failed to send webcam data:", err);
      setFeedback("🚫 Error sending image.");
    }
  };

  return (
    <div className="webcam-capture">
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={250}
      />
      <div className="webcam-controls">
        <button onClick={captureAndSend}>Analyze Expression</button>
        <p>{feedback}</p>
      </div>
    </div>
  );
};

export default WebcamCapture;
