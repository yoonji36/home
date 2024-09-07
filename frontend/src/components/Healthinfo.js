import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const HealthInfo = () => {
  const [weight, setWeight] = useState('');
  const [height, setHeight] = useState('');
  const [bloodSugar, setBloodSugar] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const userId = localStorage.getItem('user_id');

    fetch('/submit_health_info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, weight, height, blood_sugar: bloodSugar }),
    })
      .then(() => {
        navigate('/upload');
      });
  };

  return (
    <div>
      <h1>Health Information</h1>
      <form onSubmit={handleSubmit}>
        <label>Weight (kg):</label>
        <input
          type="number"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
          required
        />
        <br />
        <label>Height (cm):</label>
        <input
          type="number"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
          required
        />
        <br />
        <label>Blood Sugar (mg/dL):</label>
        <input
          type="number"
          value={bloodSugar}
          onChange={(e) => setBloodSugar(e.target.value)}
          required
        />
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default HealthInfo;
