import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function BloomsChart({ data }) {
  const { distribution } = data;

  const levels = ['Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create'];
  
  const chartData = {
    labels: levels,
    datasets: [
      {
        label: 'Number of Questions',
        data: levels.map(level => distribution[level] || 0),
        backgroundColor: [
          '#667eea',
          '#764ba2',
          '#f093fb',
          '#4facfe',
          '#43e97b',
          '#fa709a',
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
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `Questions: ${context.parsed.y}`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
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
        Bloom's Taxonomy Distribution
      </h3>
      <div style={{ height: 'clamp(250px, 50vw, 300px)' }}>
        <Bar data={chartData} options={options} />
      </div>
      <div style={{
        marginTop: '20px',
        padding: '15px',
        background: '#f8f9ff',
        borderRadius: '8px',
        fontSize: 'clamp(0.75rem, 2vw, 0.9rem)',
        color: '#666'
      }}>
        <strong>Goal:</strong> Questions across multiple cognitive levels
      </div>
    </div>
  );
}

export default BloomsChart;
