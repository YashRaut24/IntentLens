import React from 'react';
import './AnalysisHistory.css';

export default function AnalysisHistory({
  analyses = [],
  onSelectAnalysis,
  onDeleteAnalysis,
  onClearHistory,
  onNavigateAnalyze,
}) {
  if (!analyses || analyses.length === 0) {
    return (
      <div className="empty-history-card">
        <div className="empty-icon-ring">✦</div>
        <h3 className="empty-title">No learning analyses saved yet.</h3>
        <p className="empty-subtext">
          Describe a learning goal naturally to extract your target, known skills, potential gaps, and recommended starting point.
        </p>
        <button className="btn-primary" onClick={onNavigateAnalyze}>
          Find Your First Starting Point
        </button>
      </div>
    );
  }

  const formatDate = (isoString) => {
    if (!isoString) return 'Just now';
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });
    } catch {
      return 'Recent';
    }
  };

  return (
    <div className="analysis-history-container">
      <div className="history-header-actions">
        <div className="history-meta">
          <span className="history-badge">SAVED LEARNING GOALS</span>
          <h2 className="history-title">Analysis History</h2>
          <span className="history-count">{analyses.length} queries analyzed</span>
        </div>
        <button
          className="btn-clear-history"
          onClick={onClearHistory}
          title="Clear all saved learning analyses"
        >
          Clear History
        </button>
      </div>

      <div className="history-list">
        {analyses.map((item) => {
          const goalTopic = item.goal?.topic || (item.topics && item.topics[0]) || 'General Goal';
          const startingPointTitle = item.startingPoint?.title || 'Starting Point';
          const knownList = item.knownSkills && item.knownSkills.length > 0 ? item.knownSkills.join(', ') : 'None stated';

          return (
            <div key={item._id || item.createdAt} className="history-row-card">
              <div className="history-col-main" onClick={() => onSelectAnalysis(item)}>
                <p className="history-query-text">"{item.query}"</p>
                <div className="history-data-grid">
                  <div className="data-cell">
                    <span className="cell-label">Goal:</span>
                    <span className="cell-value goal-highlight">{goalTopic}</span>
                  </div>
                  <div className="data-cell">
                    <span className="cell-label">Known Skills:</span>
                    <span className="cell-value">{knownList}</span>
                  </div>
                  <div className="data-cell">
                    <span className="cell-label">Starting Point:</span>
                    <span className="cell-value start-highlight">{startingPointTitle}</span>
                  </div>
                  <div className="data-cell">
                    <span className="cell-label">Level:</span>
                    <span className="cell-value">{item.learningLevel || 'Intermediate'}</span>
                  </div>
                  <div className="data-cell">
                    <span className="cell-label">Date:</span>
                    <span className="cell-value">{formatDate(item.createdAt)}</span>
                  </div>
                </div>
              </div>

              <div className="history-col-status">
                <div className="history-actions">
                  <button
                    className="btn-row-action btn-view"
                    onClick={() => onSelectAnalysis(item)}
                    title="View full breakdown"
                  >
                    View Analysis
                  </button>
                  <button
                    className="btn-row-action btn-delete"
                    onClick={() => onDeleteAnalysis(item._id)}
                    title="Delete this analysis"
                    aria-label="Delete analysis"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
