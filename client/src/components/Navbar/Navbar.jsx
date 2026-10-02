import React, { useState } from 'react';
import './Navbar.css';

export default function Navbar({ activePage, setActivePage }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'analyze', label: 'Ask a Question' },
    { id: 'history', label: 'History' },
    { id: 'about', label: 'How It Works' },
  ];

  const handleNavClick = (pageId) => {
    setActivePage(pageId);
    setMobileOpen(false);
  };

  return (
    <nav className="navbar" aria-label="Main Navigation">
      <div className="navbar-container">
        <div className="navbar-brand" onClick={() => handleNavClick('home')}>
          <div className="brand-badge">IL</div>
          <span className="brand-name">
            Intent<span className="brand-accent">Lens</span>
          </span>
        </div>

        <button
          className="mobile-toggle"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle navigation menu"
        >
          <span className={`hamburger-bar ${mobileOpen ? 'open' : ''}`}></span>
          <span className={`hamburger-bar ${mobileOpen ? 'open' : ''}`}></span>
        </button>

        <div className={`navbar-links ${mobileOpen ? 'mobile-visible' : ''}`}>
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-link ${activePage === item.id ? 'active' : ''}`}
              onClick={() => handleNavClick(item.id)}
            >
              {item.label}
            </button>
          ))}
          <button
            className="nav-cta-button"
            onClick={() => handleNavClick('analyze')}
          >
            Launch Analyzer
          </button>
        </div>
      </div>
    </nav>
  );
}
