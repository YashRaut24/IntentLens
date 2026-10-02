import React, { useState } from 'react';
import './QueryInput.css';

const SAMPLE_QUERIES = [
  "I know Python and basic machine learning. I want to get into LLMs but don't know what I should learn first.",
  "I want to learn React. I already know HTML, CSS and basic JavaScript.",
  "I want to build an AI chatbot using Python, but I've never worked with NLP.",
  "I'm preparing for a machine learning internship. I know Python and sklearn but I'm weak at statistics.",
  "I know Java and basic DSA. I want to start competitive programming but I'm not good at dynamic programming.",
  "I like technology.",
];

export default function QueryInput({ onSubmit, isLoading, errorMessage }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;
    onSubmit(query.trim());
  };

  const handleSelectSample = (sample) => {
    setQuery(sample);
  };

  return (
    <div className="query-input-container">
      <div className="input-heading-group">
        <span className="input-label-tag">NATURAL LANGUAGE LEARNING INTELLIGENCE</span>
        <h2 className="input-main-heading">What do you want to learn?</h2>
        <p className="input-subtext">
          Describe your goal naturally. Mention what you already know, what you're struggling with, or what you're preparing for.
        </p>
      </div>

      <form className="query-form" onSubmit={handleSubmit}>
        <div className="textarea-wrapper">
          <textarea
            id="student-query-input"
            className="query-textarea"
            rows="4"
            placeholder="I know Python and basic ML. I want to learn LLMs but don't know where to start."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
            aria-label="Natural language learning goal"
          />
          <div className="textarea-footer">
            <span className="char-count">{query.length} characters</span>
            <button
              type="submit"
              className="btn-analyze-submit"
              disabled={isLoading || !query.trim()}
            >
              {isLoading ? 'Analyzing...' : 'Find My Starting Point'}
            </button>
          </div>
        </div>

        {errorMessage && (
          <div className="query-error-banner" role="alert">
            <span className="error-icon">!</span>
            <span className="error-text">{errorMessage}</span>
          </div>
        )}
      </form>

      <div className="samples-container">
        <span className="samples-label">Explore sample learning queries:</span>
        <div className="samples-grid">
          {SAMPLE_QUERIES.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              className="sample-chip"
              onClick={() => handleSelectSample(sample)}
              disabled={isLoading}
            >
              {sample}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
