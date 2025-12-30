import React, { useState } from 'react';

function UploadForm({ onAnalyze, error }) {
  const [examFile, setExamFile] = useState(null);
  const [syllabusFile, setSyllabusFile] = useState(null);

  const handleExamFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setExamFile(file);
    }
  };

  const handleSyllabusFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSyllabusFile(file);
    }
  };

  const handleSubmit = () => {
    if (examFile && syllabusFile) {
      onAnalyze(examFile, syllabusFile);
    }
  };

  const isReady = examFile && syllabusFile;

  return (
    <div className="upload-section">
      <h2>Upload Your Files</h2>
      
      <div className="file-upload-container">
        <div className="file-upload-box">
          <h3>📄 Exam Paper</h3>
          <input
            type="file"
            id="exam-file"
            accept=".pdf,.txt"
            onChange={handleExamFileChange}
          />
          <label htmlFor="exam-file" className="file-upload-label">
            {examFile ? (
              <div className="file-info">✓ {examFile.name}</div>
            ) : (
              <>
                <div style={{ fontSize: '3rem', marginBottom: '10px' }}>📤</div>
                <div>Click to upload exam paper</div>
                <div style={{ fontSize: '0.85rem', color: '#999', marginTop: '5px' }}>
                  PDF or TXT format
                </div>
              </>
            )}
          </label>
        </div>

        <div className="file-upload-box">
          <h3>📚 Course Syllabus</h3>
          <input
            type="file"
            id="syllabus-file"
            accept=".pdf,.txt"
            onChange={handleSyllabusFileChange}
          />
          <label htmlFor="syllabus-file" className="file-upload-label">
            {syllabusFile ? (
              <div className="file-info">✓ {syllabusFile.name}</div>
            ) : (
              <>
                <div style={{ fontSize: '3rem', marginBottom: '10px' }}>📤</div>
                <div>Click to upload syllabus</div>
                <div style={{ fontSize: '0.85rem', color: '#999', marginTop: '5px' }}>
                  PDF or TXT format
                </div>
              </>
            )}
          </label>
        </div>
      </div>

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      <button
        className="analyze-button"
        onClick={handleSubmit}
        disabled={!isReady}
      >
        {isReady ? '🚀 Analyze Paper' : '⏳ Select Both Files'}
      </button>

      <div style={{ marginTop: '30px', padding: '20px', background: '#f8f9ff', borderRadius: '12px', textAlign: 'left' }}>
        <h3 style={{ color: '#667eea', marginBottom: '15px', fontSize: 'clamp(1.1rem, 4vw, 1.3rem)' }}>📌 What This Tool Does</h3>
        <ul style={{ lineHeight: '1.8', color: '#666', fontSize: 'clamp(0.85rem, 3vw, 0.95rem)', paddingLeft: '20px' }}>
          <li>✅ Analyzes difficulty distribution using Azure OpenAI</li>
          <li>✅ Maps questions to Bloom's Taxonomy cognitive levels</li>
          <li>✅ Checks syllabus coverage using Azure AI Language</li>
          <li>✅ Detects potential bias and ambiguity</li>
          <li>✅ Provides a Fairness Score (0-100) with explanations</li>
          <li>✅ Offers actionable suggestions for improvement</li>
        </ul>
      </div>
    </div>
  );
}

export default UploadForm;
