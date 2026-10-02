import React from 'react';
import './Hero.css';

export default function Hero({ onAnalyzeClick, onExplorePipeline }) {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <div className="hero-badge">NATURAL LANGUAGE LEARNING INTELLIGENCE</div>
        <h1 className="hero-heading">
          Describe Your Goal. <br />
          <span className="serif-accent">Find Your Starting Point.</span>
        </h1>
        <p className="hero-subtitle">
          IntentLens turns natural-language learning goals into structured knowledge about what you
          want to learn, what you already know, and what foundations may come next.
        </p>

        <div className="hero-actions">
          <button className="btn-primary" onClick={onAnalyzeClick}>
            Find My Starting Point
          </button>
          <button className="btn-secondary" onClick={onExplorePipeline}>
            Explore the NLP Pipeline
          </button>
        </div>

        <div className="hero-metrics">
          <div className="metric-item">
            <span className="metric-number">Goal & Gap</span>
            <span className="metric-label">NLP Extraction</span>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-item">
            <span className="metric-number">91%</span>
            <span className="metric-label">Semantic Match</span>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-item">
            <span className="metric-number">Zero-Guess</span>
            <span className="metric-label">Lightweight Knowledge States</span>
          </div>
        </div>
      </div>

      <div className="hero-visual">
        <div className="nlp-pipeline-card">
          <div className="card-header">
            <div className="window-dots">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
            <span className="card-title-tag">STRUCTURED LEARNING EXTRACTION</span>
          </div>

          <div className="query-stage">
            <span className="stage-label">STUDENT QUERY</span>
            <div className="query-box">
              "I know Python and basic machine learning. I want to get into LLMs but don't know what I should learn first."
            </div>
          </div>

          <div className="pipeline-flow-arrow">
            <span className="arrow-line"></span>
            <span className="flow-indicator">NLP KNOWLEDGE STATE MAPPING</span>
          </div>

          <div className="structured-output-stage">
            <span className="stage-label">EXTRACTED LEARNER PROFILE</span>
            <div className="output-grid">
              <div className="output-row">
                <span className="field-name">Your Goal</span>
                <span className="field-value accent-highlight">LLMs</span>
              </div>
              <div className="output-row">
                <span className="field-name">You Already Know</span>
                <span className="field-value">✓ Python, ✓ Machine Learning</span>
              </div>
              <div className="output-row">
                <span className="field-name">Potential Gaps</span>
                <span className="field-value">Deep Learning, Attention, Transformers</span>
              </div>
              <div className="output-row">
                <span className="field-name">Your Starting Point</span>
                <span className="field-value accent-highlight">Deep Learning Fundamentals</span>
              </div>
              <div className="output-row">
                <span className="field-name">Learning Context</span>
                <span className="field-value level-pill">Skill Development</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
