import React, { useState } from 'react';
import EILPanel from './EILPanel';
import SymbolicInsightPanel from './SymbolicInsightPanel';
import EmotionGraph from './EmotionGraph';
import AudioRecorder from './AudioRecorder';
import WebcamCapture from './WebcamCapture';

const DiagnosticPanel = () => {
  const [visible, setVisible] = useState(false);

  return (
    <div className="diagnostic-wrapper">
      <button className="diagnostic-toggle" onClick={() => setVisible(!visible)}>
        {visible ? "▾ Hide Diagnostics" : "▸ Show Diagnostics"}
      </button>

      {visible && (
        <div className="diagnostic-panel">
          <EmotionGraph />
          <EILPanel />
          <SymbolicInsightPanel />
          <AudioRecorder />
          <WebcamCapture />
        </div>
      )}
    </div>
  );
};

export default DiagnosticPanel;
