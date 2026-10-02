import React, { useState } from 'react';
import QueryInput from '../../components/QueryInput/QueryInput';
import LoadingAnalysis from '../../components/LoadingAnalysis/LoadingAnalysis';
import IntentResult from '../../components/IntentResult/IntentResult';
import { analyzeQuery } from '../../services/api';
import './Analyze.css';

export default function Analyze({ onAnalysisSaved }) {
  const [isLoading, setIsLoading] = useState(false);
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleAnalyzeSubmit = async (queryText) => {
    setIsLoading(true);
    setErrorMessage('');
    setCurrentAnalysis(null);

    try {
      const result = await analyzeQuery(queryText);
      setCurrentAnalysis(result);
      if (onAnalysisSaved) {
        onAnalysisSaved(result);
      }
    } catch (err) {
      setErrorMessage(err.message || 'An unexpected error occurred during NLP analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="analyze-page-container">
      {/* Input section */}
      <QueryInput
        onSubmit={handleAnalyzeSubmit}
        isLoading={isLoading}
        errorMessage={errorMessage}
      />

      {/* Loading state */}
      {isLoading && <LoadingAnalysis />}

      {/* Result view */}
      {currentAnalysis && !isLoading && (
        <IntentResult analysis={currentAnalysis} />
      )}
    </div>
  );
}
