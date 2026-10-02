import React, { useState, useEffect } from 'react';
import AnalysisHistory from '../../components/AnalysisHistory/AnalysisHistory';
import IntentResult from '../../components/IntentResult/IntentResult';
import { fetchHistory, deleteAnalysisById, clearAllHistory } from '../../services/api';
import './History.css';

export default function History({ onNavigatePage }) {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [feedbackMsg, setFeedbackMsg] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchHistory();
      setAnalyses(data);
    } catch (err) {
      console.error('History fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDelete = async (id) => {
    if (!id) return;
    try {
      await deleteAnalysisById(id);
      setAnalyses((prev) => prev.filter((item) => item._id !== id));
      if (selectedAnalysis && selectedAnalysis._id === id) {
        setSelectedAnalysis(null);
      }
      setFeedbackMsg('Record removed from database.');
      setTimeout(() => setFeedbackMsg(''), 3000);
    } catch (err) {
      alert(`Delete failed: ${err.message}`);
    }
  };

  const handleClear = async () => {
    if (!window.confirm('Are you sure you want to clear all analysis history?')) return;
    try {
      await clearAllHistory();
      setAnalyses([]);
      setSelectedAnalysis(null);
      setFeedbackMsg('All history records cleared.');
      setTimeout(() => setFeedbackMsg(''), 3000);
    } catch (err) {
      alert(`Clear failed: ${err.message}`);
    }
  };

  return (
    <div className="history-page-container">
      {feedbackMsg && (
        <div className="feedback-banner" role="status">
          {feedbackMsg}
        </div>
      )}

      {/* Selected Modal / Detail Card */}
      {selectedAnalysis && (
        <div className="selected-analysis-preview">
          <div className="preview-header">
            <span className="preview-title">INSPECTING STORED RECORD</span>
            <button
              className="btn-close-preview"
              onClick={() => setSelectedAnalysis(null)}
            >
              Close Inspection ✕
            </button>
          </div>
          <IntentResult analysis={selectedAnalysis} />
        </div>
      )}

      {loading ? (
        <div className="history-loading-indicator">
          <div className="pulse-dot"></div>
          <span>Loading historical queries from MongoDB...</span>
        </div>
      ) : (
        <AnalysisHistory
          analyses={analyses}
          onSelectAnalysis={(item) => {
            setSelectedAnalysis(item);
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}
          onDeleteAnalysis={handleDelete}
          onClearHistory={handleClear}
          onNavigateAnalyze={() => onNavigatePage('analyze')}
        />
      )}
    </div>
  );
}
