import React, { useEffect, useState } from 'react';

const EILPanel = () => {
  const [eilData, setEilData] = useState({});

  useEffect(() => {
    const fetchEIL = async () => {
      try {
        const res = await fetch('http://localhost:5000/api/eil-state');
        const data = await res.json();
        setEilData(data || {});
      } catch (err) {
        console.error("Failed to fetch EIL state:", err);
      }
    };

    fetchEIL();
    const interval = setInterval(fetchEIL, 3000); // refresh every 3s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="eil-panel">
      <h4>🧠 EIL Signal (Raw)</h4>
      <pre>{JSON.stringify(eilData, null, 2)}</pre>
    </div>
  );
};

export default EILPanel;
