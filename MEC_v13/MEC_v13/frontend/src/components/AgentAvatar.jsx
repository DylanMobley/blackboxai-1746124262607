import React from 'react';
import './AgentAvatar.css';

const AgentAvatar = ({ persona }) => {
  const imageMap = {
    "reflective_mentor": "/avatars/mentor.png",
    "soothing_ally": "/avatars/ally.png",
    "direct_analyst": "/avatars/analyst.png",
    "playful_muse": "/avatars/muse.png"
  };

  return (
    <div className="agent-avatar">
      <img src={imageMap[persona] || imageMap["soothing_ally"]} alt="AI Persona" />
      <div className="persona-label">{persona.replace('_', ' ')}</div>
    </div>
  );
};

export default AgentAvatar;
