import React, { useState } from 'react';
import axios from 'axios';
import UploadForm from './components/UploadForm';
import ResultsDisplay from './components/ResultsDisplay';
import { API_BASE_URL } from './config';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (examFile, syllabusFile) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('exam_paper', examFile);
      formData.append('syllabus', syllabusFile);

      const response = await axios.post(`${API_BASE_URL}/api/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to analyze exam paper. Please check your files and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🎓 FairExam AI</h1>
        <p>AI-Powered Exam Paper Fairness & Bias Detection System</p>
        <span className="badge">Microsoft Imagine Cup 2026</span>
      </header>

      <div className="content">
        {!results && !loading && (
          <UploadForm onAnalyze={handleAnalyze} error={error} />
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyzing exam paper with Azure AI...</p>
            <p style={{ fontSize: '0.9rem', color: '#999', marginTop: '10px' }}>
              This may take 30-60 seconds
            </p>
          </div>
        )}

        {results && (
          <ResultsDisplay results={results} onReset={handleReset} />
        )}
      </div>
    </div>
  );
}

export default App;
