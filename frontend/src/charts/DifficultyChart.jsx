import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

function DifficultyChart({ data }) {
  const { distribution, total_questions } = data;

  const chartData = {
    labels: ['Easy', 'Medium', 'Hard'],
    datasets: [
      {
        data: [
          distribution.Easy || 0,
          distribution.Medium || 0,
          distribution.Hard || 0,
        ],
        backgroundColor: [
          '#28a745',
          '#ffc107',
          '#dc3545',
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
            const percentage = total_questions > 0 
              ? ((value / total_questions) * 100).toFixed(1)
              : 0;
            return `${label}: ${value} questions (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      padding: 'clamp(15px, 4vw, 25px)',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
    }}>
      <h3 style={{ color: '#667eea', marginBottom: '20px', textAlign: 'center', fontSize: 'clamp(1rem, 4vw, 1.2rem)' }}>
        Difficulty Distribution
      </h3>
      <div style={{ maxWidth: '300px', margin: '0 auto', minHeight: '250px' }}>
        <Pie data={chartData} options={options} />
      </div>
      <div style={{
        marginTop: '20px',
        padding: '15px',
        background: '#f8f9ff',
        borderRadius: '8px',
        fontSize: 'clamp(0.75rem, 2vw, 0.9rem)',
        color: '#666'
      }}>
        <strong>Ideal:</strong> 30% Easy, 50% Medium, 20% Hard
      </div>
    </div>
  );
}

export default DifficultyChart;
