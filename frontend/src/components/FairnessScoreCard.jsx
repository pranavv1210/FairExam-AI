import React from 'react';

function FairnessScoreCard({ score, interpretation, componentScores }) {
  // Determine color based on score
  const getScoreColor = (score) => {
    if (score >= 85) return '#28a745';
    if (score >= 70) return '#5cb85c';
    if (score >= 55) return '#ffc107';
    if (score >= 40) return '#ff9800';
    return '#dc3545';
  };

  const scoreColor = getScoreColor(score);

  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      borderRadius: '16px',
      padding: '40px',
      marginBottom: '30px',
      color: 'white',
      boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)'
    }}>
      <h2 style={{ marginBottom: '20px', textAlign: 'center', fontSize: '1.5rem' }}>
        Fairness Score
      </h2>
      
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '30px',
        textAlign: 'center',
        marginBottom: '20px'
      }}>
        <div style={{
          fontSize: 'clamp(3rem, 15vw, 5rem)',
          fontWeight: 'bold',
          color: scoreColor,
          lineHeight: '1'
        }}>
          {score}
        </div>
        <div style={{ fontSize: '1.2rem', color: '#666', marginTop: '10px' }}>
          out of 100
        </div>
      </div>

      <div style={{
        background: 'rgba(255, 255, 255, 0.15)',
        borderRadius: '12px',
        padding: '20px',
        marginBottom: '20px'
      }}>
        <p style={{ fontSize: '1.05rem', lineHeight: '1.6' }}>
          {interpretation}
        </p>
      </div>

      {/* Component Breakdown */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
        gap: '15px'
      }}>
        {Object.entries(componentScores).map(([key, data]) => (
          <div key={key} style={{
            background: 'rgba(255, 255, 255, 0.15)',
            borderRadius: '12px',
            padding: '15px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: 'clamp(0.75rem, 2vw, 0.9rem)', marginBottom: '10px', opacity: 0.9 }}>
              {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </div>
            <div style={{ fontSize: 'clamp(1.5rem, 5vw, 2rem)', fontWeight: 'bold', marginBottom: '5px' }}>
              {data.score.toFixed(1)}
            </div>
            <div style={{ fontSize: 'clamp(0.7rem, 1.5vw, 0.85rem)', opacity: 0.8 }}>
              W:{data.weight}% C:{data.weighted_contribution}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FairnessScoreCard;
