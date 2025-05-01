import React from 'react';

const PersonaSwitcher = ({ persona, setPersona }) => {
  const personas = ["soothing_ally", "reflective_mentor", "direct_analyst", "playful_muse"];

  return (
    <div className="persona-switcher">
      <label>🧠 Persona</label>
      <select value={persona} onChange={e => setPersona(e.target.value)}>
        {personas.map(p => <option key={p} value={p}>{p.replace('_', ' ')}</option>)}
      </select>
    </div>
  );
};

export default PersonaSwitcher;
