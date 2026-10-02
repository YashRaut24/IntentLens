import React from 'react';
import './ConfidenceMeter.css';

export default function ConfidenceMeter({ confidence, label }) {
  const safeConfidence = Math.max(0, Math.min(100, confidence || 0));

  const getStatusColor = () => {
    if (safeConfidence >= 80) return 'status-high';
    if (safeConfidence >= 60) return 'status-medium';
    return 'status-low';
  };

  const getFriendlyLabel = () => {
    if (safeConfidence >= 80) return 'High Certainty';
    if (safeConfidence >= 60) return 'Good Match';
    return 'General Match';
  };

  return (
    <div className="confidence-meter-container">
      <div className="meter-header">
        <span className="meter-title">SYSTEM CERTAINTY</span>
        <div className="meter-badge-group">
          <span className={`confidence-tier ${getStatusColor()}`}>
            {getFriendlyLabel()}
          </span>
          <span className="confidence-number">{safeConfidence}%</span>
        </div>
      </div>

      <div className="meter-track">
        <div
          className={`meter-bar ${getStatusColor()}`}
          style={{ width: `${safeConfidence}%` }}
        ></div>
      </div>
      <span className="meter-footnote">
        Determined by comparing your question with real student learning patterns
      </span>
    </div>
  );
}
