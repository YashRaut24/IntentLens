import React from 'react';
import './TopicTags.css';

export default function TopicTags({ topics = [], relatedConcepts = [], keywords = [] }) {
  return (
    <div className="topic-tags-wrapper">
      {/* Primary Topics */}
      <div className="tag-group">
        <span className="tag-group-label">MAIN TOPIC</span>
        <div className="tag-chips-row">
          {topics && topics.length > 0 ? (
            topics.map((t, idx) => (
              <span key={idx} className="topic-tag primary-topic">
                {t}
              </span>
            ))
          ) : (
            <span className="tag-empty">General topic</span>
          )}
        </div>
      </div>

      {/* Related Concepts */}
      {relatedConcepts && relatedConcepts.length > 0 && (
        <div className="tag-group">
          <span className="tag-group-label">CONCEPTS YOU ALREADY KNOW OR MENTIONED</span>
          <div className="tag-chips-row">
            {relatedConcepts.map((rc, idx) => (
              <span key={idx} className="topic-tag related-topic">
                {rc}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Extracted Keywords */}
      <div className="tag-group">
        <span className="tag-group-label">IMPORTANT TERMS IN YOUR QUESTION</span>
        <div className="tag-chips-row">
          {keywords && keywords.length > 0 ? (
            keywords.map((kw, idx) => (
              <span key={idx} className="keyword-chip">
                #{kw}
              </span>
            ))
          ) : (
            <span className="tag-empty">No key terms highlighted</span>
          )}
        </div>
      </div>
    </div>
  );
}
