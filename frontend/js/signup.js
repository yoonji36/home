import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './signup.css';

const Signup = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    height: '',
    weight: '',
    bloodPressure: '',
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('/signup/', formData);
      if (response.data.success) {
        navigate('/main');
      }
    } catch (error) {
      console.error('Error during signup:', error);
    }
  };

  return (
    <div className="signup-container">
      <h2>회원 가입</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">ID:</label>
          <input
            type="text"
            id="username"
            name="username"
            className="form-control"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">비밀번호:</label>
          <input
            type="password"
            id="password"
            name="password"
            className="form-control"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="height" className="form-label">키 (cm):</label>
          <input
            type="text"
            id="height"
            name="height"
            className="form-control"
            value={formData.height}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="weight" className="form-label">몸무게 (kg):</label>
          <input
            type="text"
            id="weight"
            name="weight"
            className="form-control"
            value={formData.weight}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="bloodPressure" className="form-label">혈압:</label>
          <input
            type="text"
            id="bloodPressure"
            name="bloodPressure"
            className="form-control"
            value={formData.bloodPressure}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-custom">회원 가입</button>
      </form>
    </div>
  );
};

export default Signup;
