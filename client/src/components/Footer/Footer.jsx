import React from 'react';
import './Footer.css';

export default function Footer({ onNavigatePage }) {
  return (
    <footer className="footer-container">
      <div className="footer-content">
        <div className="footer-brand-section">
          <div className="footer-logo">
            <span className="footer-logo-badge">IL</span>
            <span className="footer-logo-title">IntentLens</span>
          </div>
          <p className="footer-tagline">
            Student Learning Intent Intelligence System. Transforming natural-language
            student questions into clear, structured learning paths.
          </p>
          <span className="academic-badge">Academic NLP Mini Project • Semester 7</span>
        </div>

        <div className="footer-links-group">
          <div className="footer-column">
            <span className="col-header">EXPLORE</span>
            <button className="foot-link" onClick={() => onNavigatePage('home')}>Home</button>
            <button className="foot-link" onClick={() => onNavigatePage('analyze')}>Ask a Question</button>
            <button className="foot-link" onClick={() => onNavigatePage('history')}>Question History</button>
            <button className="foot-link" onClick={() => onNavigatePage('about')}>How It Works</button>
          </div>

          <div className="footer-column">
            <span className="col-header">INTELLIGENCE</span>
            <span className="foot-static-item">Natural Language Processing</span>
            <span className="foot-static-item">Machine Learning Classification</span>
            <span className="foot-static-item">Sentence Meaning Models</span>
            <span className="foot-static-item">Concept & Skill Extraction</span>
          </div>

          <div className="footer-column">
            <span className="col-header">PLATFORM</span>
            <span className="foot-static-item">Independent & Standalone</span>
            <span className="foot-static-item">Student-Centered Experience</span>
            <span className="foot-static-item">100% Private & Local</span>
            <span className="foot-static-item">Fast Response Times</span>
          </div>
        </div>
      </div>

      <div className="footer-bottom-bar">
        <span className="copyright-text">
          IntentLens © {new Date().getFullYear()} • Student Learning Intent Intelligence System
        </span>
        <span className="stack-status">Engine: Local AI & Language Processing</span>
      </div>
    </footer>
  );
}
