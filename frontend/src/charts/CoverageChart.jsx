import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

function CoverageChart({ data }) {
  const { coverage_percentage, covered_topics, total_topics } = data;

  const uncovered = total_topics - covered_topics;

  const chartData = {
    labels: ['Covered Topics', 'Not Covered'],
    datasets: [
      {
        data: [covered_topics, uncovered],
        backgroundColor: [
          '#667eea',
          '#e0e0e0',
        ],
        borderColor: 'white',
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 15,
          font: {
            size: 13,
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed || 0;
            return `${label}: ${value} topics`;
          },
        },
      },
    },
  };

  const getCoverageColor = (percentage) => {
    if (percentage >= 80) return '#28a745';
    if (percentage >= 60) return '#ffc107';
    return '#dc3545';
  };

  return (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      padding: 'clamp(15px, 4vw, 25px)',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
    }}>
      <h3 style={{ color: '#667eea', marginBottom: '20px', textAlign: 'center', fontSize: 'clamp(1rem, 4vw, 1.2rem)' }}>
        Syllabus Coverage
      </h3>
      <div style={{ maxWidth: '300px', margin: '0 auto', minHeight: '250px' }}>
        <Doughnut data={chartData} options={options} />
      </div>
      <div style={{
        marginTop: '20px',
        textAlign: 'center'
      }}>
        <div style={{
          fontSize: 'clamp(1.8rem, 6vw, 2.5rem)',
          fontWeight: 'bold',
          color: getCoverageColor(coverage_percentage)
        }}>
          {coverage_percentage.toFixed(1)}%
        </div>
        <div style={{
          fontSize: 'clamp(0.75rem, 2vw, 0.9rem)',
          color: '#666',
          marginTop: '5px'
        }}>
          {covered_topics} out of {total_topics} topics covered
        </div>
      </div>
    </div>
  );
}

export default CoverageChart;
