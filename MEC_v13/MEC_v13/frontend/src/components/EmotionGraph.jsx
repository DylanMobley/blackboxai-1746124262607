import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const EmotionGraph = () => {
  const [emotionData, setEmotionData] = useState({});

  useEffect(() => {
    const fetchEmotions = async () => {
      try {
        const res = await fetch('http://localhost:5000/api/emotion-state');
        const data = await res.json();
        setEmotionData(data || {});
      } catch (err) {
        console.error("Failed to load emotion state:", err);
      }
    };

    fetchEmotions();
    const interval = setInterval(fetchEmotions, 3000); // refresh every 3 sec

    return () => clearInterval(interval);
  }, []);

  const labels = Object.keys(emotionData);
  const values = Object.values(emotionData);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Emotion Confidence',
        data: values,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      }
    ]
  };

  const options = {
    indexAxis: 'y',
    scales: {
      x: { beginAtZero: true, max: 1.0 }
    }
  };

  return (
    <div className="emotion-graph">
      <h4>🧠 Emotional State (ESIL)</h4>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default EmotionGraph;
