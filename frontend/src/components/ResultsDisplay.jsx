import React from 'react';
import FairnessScoreCard from './FairnessScoreCard';
import DifficultyChart from '../charts/DifficultyChart';
import BloomsChart from '../charts/BloomsChart';
import CoverageChart from '../charts/CoverageChart';

function ResultsDisplay({ results, onReset }) {
  const {
    fairness_score,
    interpretation,
    component_scores,
    suggestions,
    difficulty_analysis,
    blooms_analysis,
    coverage_analysis,
    bias_analysis,
    exam_metadata
  } = results;

  return (
    <div className="results-container">
      <button className="back-button" onClick={onReset}>
        ← Analyze Another Paper
      </button>

      <div style={{ marginBottom: '30px' }}>
        <h2 style={{ color: '#333', marginBottom: '10px', fontSize: 'clamp(1.3rem, 5vw, 1.8rem)' }}>
          Analysis Results
        </h2>
        <p style={{ color: '#666', fontSize: 'clamp(0.8rem, 2vw, 0.95rem)' }}>
          Exam: <strong>{exam_metadata.exam_filename}</strong> | 
          Questions: <strong>{exam_metadata.total_questions}</strong>
        </p>
      </div>

      {/* Fairness Score Card */}
      <FairnessScoreCard
        score={fairness_score}
        interpretation={interpretation}
        componentScores={component_scores}
      />

      {/* Suggestions Section */}
      <div style={{
        background: '#fff3cd',
        border: '2px solid #ffc107',
        borderRadius: '12px',
        padding: 'clamp(15px, 4vw, 25px)',
        marginBottom: '30px'
      }}>
        <h3 style={{ color: '#856404', marginBottom: '15px', display: 'flex', alignItems: 'center', fontSize: 'clamp(1.1rem, 4vw, 1.3rem)' }}>
          <span style={{ fontSize: '1.5rem', marginRight: '10px' }}>💡</span>
          Improvement Suggestions
        </h3>
        <ul style={{ lineHeight: '2', color: '#856404', paddingLeft: '20px', fontSize: 'clamp(0.8rem, 2vw, 0.95rem)' }}>
          {suggestions.map((suggestion, index) => (
            <li key={index}>{suggestion}</li>
          ))}
        </ul>
      </div>

      {/* Charts Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '20px',
        marginBottom: '30px'
      }}>
        <DifficultyChart data={difficulty_analysis} />
        <BloomsChart data={blooms_analysis} />
        <CoverageChart data={coverage_analysis} />
      </div>

      {/* Bias Analysis Section */}
      {bias_analysis && (
        <div style={{
          background: bias_analysis.bias_detected ? '#fee' : '#efe',
          border: `2px solid ${bias_analysis.bias_detected ? '#f88' : '#8f8'}`,
          borderRadius: '12px',
          padding: 'clamp(15px, 4vw, 25px)',
          marginBottom: '30px'
        }}>
          <h3 style={{
            color: bias_analysis.bias_detected ? '#c33' : '#383',
            marginBottom: '15px',
            fontSize: 'clamp(1.1rem, 4vw, 1.3rem)'
          }}>
            {bias_analysis.bias_detected ? '⚠️ Bias Analysis' : '✅ Bias Analysis'}
          </h3>
          
          {bias_analysis.issues && bias_analysis.issues.length > 0 && (
            <div style={{ marginBottom: '15px' }}>
              <strong>Issues Found:</strong>
              <ul style={{ marginTop: '10px', paddingLeft: '20px' }}>
                {bias_analysis.issues.map((issue, index) => (
                  <li key={index}>{issue}</li>
                ))}
              </ul>
            </div>
          )}

          {bias_analysis.fairness_indicators && (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
              gap: '15px',
              marginTop: '15px'
            }}>
              {Object.entries(bias_analysis.fairness_indicators).map(([key, value]) => (
                <div key={key} style={{
                  background: 'white',
                  padding: '15px',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: 'clamp(0.7rem, 2vw, 0.9rem)', color: '#666', marginBottom: '5px' }}>
                    {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </div>
                  <div style={{ fontSize: 'clamp(1.2rem, 4vw, 1.5rem)', fontWeight: 'bold', color: '#667eea' }}>
                    {value}%
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Detailed Coverage */}
      <div style={{
        background: '#f8f9ff',
        borderRadius: '12px',
        padding: 'clamp(15px, 4vw, 25px)',
        marginBottom: '30px'
      }}>
        <h3 style={{ color: '#667eea', marginBottom: '20px', fontSize: 'clamp(1.1rem, 4vw, 1.3rem)' }}>
          📊 Detailed Topic Coverage
        </h3>
        
        <div style={{ marginBottom: '20px', fontSize: 'clamp(0.8rem, 2vw, 0.95rem)' }}>
          <strong>Coverage: </strong>
          {coverage_analysis.covered_topics} out of {coverage_analysis.total_topics} topics 
          ({coverage_analysis.coverage_percentage}%)
        </div>

        {coverage_analysis.over_represented && coverage_analysis.over_represented.length > 0 && (
          <div style={{ marginBottom: '15px', fontSize: 'clamp(0.8rem, 2vw, 0.95rem)' }}>
            <strong style={{ color: '#dc3545' }}>Over-Represented Topics:</strong>
            <div style={{ marginTop: '5px', color: '#666', wordBreak: 'break-word' }}>
              {coverage_analysis.over_represented.join(', ')}
            </div>
          </div>
        )}

        {coverage_analysis.ignored_topics && coverage_analysis.ignored_topics.length > 0 && (
          <div style={{ fontSize: 'clamp(0.8rem, 2vw, 0.95rem)' }}>
            <strong style={{ color: '#ffc107' }}>Not Covered:</strong>
            <div style={{ marginTop: '5px', color: '#666', wordBreak: 'break-word' }}>
              {coverage_analysis.ignored_topics.join(', ')}
            </div>
          </div>
        )}

        {coverage_analysis.topic_coverage && (
          <div style={{ marginTop: '20px' }}>
            <strong>Questions per Topic:</strong>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
              gap: '10px',
              marginTop: '10px'
            }}>
              {Object.entries(coverage_analysis.topic_coverage).map(([topic, count]) => (
                <div key={topic} style={{
                  background: 'white',
                  padding: '10px',
                  borderRadius: '8px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  gap: '5px'
                }}>
                  <span style={{ fontSize: 'clamp(0.75rem, 2vw, 0.9rem)', color: '#666', wordBreak: 'break-word' }}>{topic}</span>
                  <span style={{
                    background: count > 0 ? '#667eea' : '#ddd',
                    color: 'white',
                    padding: '3px 10px',
                    borderRadius: '12px',
                    fontSize: '0.85rem',
                    fontWeight: 'bold'
                  }}>
                    {count}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Microsoft AI Badge */}
      <div style={{
        marginTop: '30px',
        padding: 'clamp(15px, 4vw, 20px)',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: '12px',
        color: 'white',
        textAlign: 'center'
      }}>
        <strong style={{ fontSize: 'clamp(0.95rem, 2vw, 1rem)' }}>Powered by Microsoft Azure AI</strong>
        <div style={{ fontSize: 'clamp(0.75rem, 1.5vw, 0.9rem)', marginTop: '5px', opacity: 0.9 }}>
          Azure OpenAI Service • Azure AI Language
        </div>
      </div>
    </div>
  );
}

export default ResultsDisplay;
