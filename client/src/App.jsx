import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import Home from './pages/Home/Home';
import Analyze from './pages/Analyze/Analyze';
import History from './pages/History/History';
import About from './pages/About/About';
import './App.css';

export default function App() {
  const getInitialPage = () => {
    const hash = window.location.hash.replace('#/', '').replace('#', '');
    if (['home', 'analyze', 'history', 'about'].includes(hash)) {
      return hash;
    }
    return 'home';
  };

  const [activePage, setActivePage] = useState(getInitialPage);

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#/', '').replace('#', '');
      if (['home', 'analyze', 'history', 'about'].includes(hash)) {
        setActivePage(hash);
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const handlePageChange = (page) => {
    setActivePage(page);
    window.location.hash = `#/${page}`;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="app-shell">
      <Navbar activePage={activePage} setActivePage={handlePageChange} />

      <main className="main-content-wrapper">
        <div className="page-container">
          {activePage === 'home' && <Home onNavigatePage={handlePageChange} />}
          {activePage === 'analyze' && <Analyze onAnalysisSaved={() => {}} />}
          {activePage === 'history' && <History onNavigatePage={handlePageChange} />}
          {activePage === 'about' && <About />}
        </div>
      </main>

      <Footer onNavigatePage={handlePageChange} />
    </div>
  );
}
