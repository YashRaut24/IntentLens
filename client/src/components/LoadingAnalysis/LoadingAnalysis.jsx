import React, { useState, useEffect } from 'react';
import './LoadingAnalysis.css';

const STAGES = [
  "Understanding your goal...",
  "Extracting what you already know...",
  "Finding learning gaps...",
  "Matching relevant prerequisites...",
  "Building your starting point...",
];

export default function LoadingAnalysis() {
  const [currentStageIdx, setCurrentStageIdx] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStageIdx((prev) => (prev + 1) % STAGES.length);
    }, 650);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-analysis-card" aria-live="polite">
      <div className="loading-badge">ANALYZING LEARNING PATH</div>
      <div className="loading-spinner-dots">
        <span className="pulse-dot"></span>
        <span className="pulse-dot"></span>
        <span className="pulse-dot"></span>
      </div>
      <h3 className="loading-stage-text">{STAGES[currentStageIdx]}</h3>
      <p className="loading-subtext">Mapping your knowledge foundation and next prerequisites</p>
    </div>
  );
}
