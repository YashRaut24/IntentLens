import React from 'react';
import './IntentResult.css';

export default function IntentResult({ analysis }) {
  if (!analysis) return null;

  const {
    query,
    isUnclear,
    message,
    goal,
    knownSkills = [],
    explicitGaps = [],
    potentialGaps = [],
    prerequisites = [],
    startingPoint,
    learningLevel = 'UNKNOWN',
    learningContext = 'SKILL_DEVELOPMENT',
    intent,
    confidence = 88,
    confidenceLabel = 'HIGH',
    explanation,
  } = analysis;

  // Render polite guidance if query had no identifiable learning goal
  if (isUnclear) {
    return (
      <div className="intent-result-card unclear-query-card" id="intent-result-view">
        <div className="unclear-badge">LEARNING GOAL UNCLEAR</div>
        <h3 className="unclear-title">We couldn't identify a clear learning goal</h3>
        <p className="unclear-desc">
          {message ||
            "Please describe what you want to learn, what you already know, or what you're struggling with."}
        </p>
        <div className="unclear-hints">
          <span className="hint-label">Try phrasing your goal like this:</span>
          <div className="hint-pill">"I know Python and want to learn LLMs but don't know where to start."</div>
          <div className="hint-pill">"I want to learn React. I already know HTML, CSS and JavaScript."</div>
          <div className="hint-pill">"I know DSA but I'm weak at dynamic programming."</div>
        </div>
      </div>
    );
  }

  const goalTitle = goal?.topic || goal?.text || 'Target Technology';
  const startTitle = startingPoint?.title || `${goalTitle} Core Concepts`;
  const startReason = startingPoint?.reason || explanation;

  const formatContext = (ctx) => {
    if (!ctx) return 'Skill Development';
    return ctx
      .replace(/_/g, ' ')
      .toLowerCase()
      .replace(/\b\w/g, (c) => c.toUpperCase());
  };

  const formatLevel = (lvl) => {
    switch (lvl) {
      case 'BEGINNER':
        return 'Beginner';
      case 'INTERMEDIATE':
        return 'Intermediate';
      case 'ADVANCED':
        return 'Advanced';
      default:
        return 'General / Unspecified';
    }
  };

  return (
    <div className="intent-result-card" id="intent-result-view">
      {/* Top Meta Bar */}
      <div className="result-top-bar">
        <div className="meta-left">
          <span className="section-kicker">LEARNING GOAL & SKILL GAP ANALYSIS</span>
          <span className="context-pill">{formatContext(learningContext)}</span>
          <span className="level-pill">{formatLevel(learningLevel)}</span>
        </div>
        <div className="meta-right">
          <span className="confidence-pill">{confidence}% CONFIDENCE</span>
        </div>
      </div>

      {/* Main Goal and Starting Point Hero */}
      <div className="result-hero-banner">
        <div className="goal-block">
          <span className="field-tag">YOUR LEARNING GOAL</span>
          <h2 className="goal-title-display">{goalTitle}</h2>
          {goal?.text && goal.text !== goalTitle && (
            <span className="goal-original-text">Target: "{goal.text}"</span>
          )}
        </div>

        <div className="starting-point-box">
          <div className="starting-point-header">
            <span className="starting-point-kicker">RECOMMENDED STARTING POINT</span>
            <span className="priority-badge">STEP 1</span>
          </div>
          <h3 className="starting-point-title">{startTitle}</h3>
          <div className="starting-point-reason-box">
            <span className="reason-label">WHY THIS STARTING POINT?</span>
            <p className="reason-text">{startReason}</p>
          </div>
        </div>
      </div>

      {/* 3-Column Knowledge State Breakdown */}
      <div className="knowledge-breakdown-grid">
        {/* Column 1: Known Skills */}
        <div className="knowledge-card known-card">
          <div className="card-top">
            <span className="card-kicker">WHAT YOU ALREADY KNOW</span>
            <span className="count-badge">{knownSkills.length}</span>
          </div>
          <div className="card-content">
            {knownSkills.length > 0 ? (
              <ul className="concept-list">
                {knownSkills.map((skill, idx) => (
                  <li key={idx} className="concept-item known-item">
                    <span className="item-icon">✓</span>
                    <span className="item-name">{skill}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="empty-state-notice">
                No existing skills were explicitly mentioned in your query.
              </p>
            )}
          </div>
        </div>

        {/* Column 2: Explicitly Mentioned Gaps */}
        <div className="knowledge-card explicit-gap-card">
          <div className="card-top">
            <span className="card-kicker">EXPLICITLY MENTIONED GAPS</span>
            <span className="count-badge">{explicitGaps.length}</span>
          </div>
          <div className="card-content">
            {explicitGaps.length > 0 ? (
              <ul className="concept-list">
                {explicitGaps.map((gap, idx) => (
                  <li key={idx} className="concept-item gap-item">
                    <span className="item-icon">•</span>
                    <span className="item-name">{gap}</span>
                    <span className="gap-tag">High Priority</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="empty-state-notice">
                No explicit struggles or weaknesses were stated.
              </p>
            )}
          </div>
        </div>

        {/* Column 3: Relevant Prerequisites & Potential Gaps */}
        <div className="knowledge-card prereq-card">
          <div className="card-top">
            <span className="card-kicker">RELEVANT PREREQUISITES</span>
            <span className="count-badge">{prerequisites.length}</span>
          </div>
          <div className="card-content">
            {prerequisites.length > 0 ? (
              <ul className="concept-list">
                {prerequisites.map((prereq, idx) => {
                  const isCovered = knownSkills.some(
                    (k) => k.toLowerCase() === prereq.toLowerCase() || prereq.toLowerCase().includes(k.toLowerCase())
                  );
                  const isWeak = explicitGaps.some(
                    (g) => g.toLowerCase() === prereq.toLowerCase() || prereq.toLowerCase().includes(g.toLowerCase())
                  );

                  return (
                    <li key={idx} className="concept-item prereq-item">
                      <span className="item-icon">{isCovered ? '✓' : '→'}</span>
                      <span className="item-name">{prereq}</span>
                      <span className={`prereq-status ${isCovered ? 'status-covered' : isWeak ? 'status-weak' : 'status-gap'}`}>
                        {isCovered ? 'Covered' : isWeak ? 'Stated Gap' : 'Potential Gap'}
                      </span>
                    </li>
                  );
                })}
              </ul>
            ) : (
              <p className="empty-state-notice">
                Prerequisites dynamically matched to your learning target.
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Visual Knowledge & Goal Progression */}
      <div className="relationship-flow-section">
        <div className="flow-header">
          <span className="flow-title">LEARNING PROGRESSION FLOW</span>
          <span className="flow-desc">Visual bridge from what you know to your goal</span>
        </div>

        <div className="flow-timeline">
          {/* Node 1: You Know */}
          <div className="timeline-node node-known">
            <div className="node-badge">1. WHAT YOU KNOW</div>
            <div className="node-content">
              {knownSkills.length > 0 ? (
                knownSkills.map((s, i) => (
                  <span key={i} className="node-chip chip-known">✓ {s}</span>
                ))
              ) : (
                <span className="node-chip chip-neutral">General Foundation</span>
              )}
            </div>
          </div>

          <div className="timeline-connector">→</div>

          {/* Node 2: Starting Point / Immediate Bridge */}
          <div className="timeline-node node-bridge">
            <div className="node-badge">2. YOUR STARTING POINT</div>
            <div className="node-content">
              <span className="node-chip chip-bridge">{startTitle}</span>
            </div>
          </div>

          <div className="timeline-connector">→</div>

          {/* Node 3: Potential Prerequisite Gaps */}
          <div className="timeline-node node-gaps">
            <div className="node-badge">3. NEXT FOUNDATIONS</div>
            <div className="node-content">
              {potentialGaps.slice(0, 3).length > 0 ? (
                potentialGaps.slice(0, 3).map((g, i) => (
                  <span key={i} className="node-chip chip-gap">• {g}</span>
                ))
              ) : (
                <span className="node-chip chip-neutral">Direct Path</span>
              )}
            </div>
          </div>

          <div className="timeline-connector">→</div>

          {/* Node 4: Target Goal */}
          <div className="timeline-node node-goal">
            <div className="node-badge">4. YOUR TARGET GOAL</div>
            <div className="node-content">
              <span className="node-chip chip-goal">★ {goalTitle}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Query Echo & Secondary Intent */}
      <div className="result-footer-row">
        <div className="footer-query-echo">
          <span className="echo-label">Query Analyzed:</span>
          <span className="echo-text">"{query}"</span>
        </div>
        {intent && (
          <div className="footer-secondary-intent">
            <span className="intent-small-label">Detected Request Type:</span>
            <span className="intent-small-badge">{intent.label || intent.name}</span>
          </div>
        )}
      </div>
    </div>
  );
}
