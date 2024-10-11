import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // CSRF 토큰 가져오기
    axios.get('http://localhost:8000/login/get-csrf-token/', { withCredentials: true });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      const response = await axios.post('http://localhost:8000/login/login/', 
        { username, password },
        {
          withCredentials: true,
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          },
        }
      );
        
      if (response.data.success) {
        localStorage.setItem('isAuthenticated', 'true');
        
        if (response.data.user_id !== undefined) {
          localStorage.setItem('userId', response.data.user_id.toString());
          localStorage.setItem('username', response.data.username);
        } else {
          console.warn('Warning: user_id not received from server');
        }
        
        const redirectUrl = '/main';
        navigate(redirectUrl);
      } else {
        setError('로그인 실패. 아이디 또는 비밀번호를 확인하세요.');
      }
    } catch (error) {
      console.error('Error during login:', error);
      if (error.response) {
        console.error('Error response:', error.response.data);
      }
      setError('로그인 중 오류가 발생했습니다. 다시 시도해주세요.');
    }
  };

  // CSRF 토큰을 쿠키에서 가져오는 함수
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const goToSignup = () => {
    navigate('/signup');
  };

  return (
    <div className="login-container">
      <h1>로그인</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">아이디:</label>
          <input
            type="text"
            id="username"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">비밀번호:</label>
          <input
            type="password"
            id="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100 mb-2">로그인</button>
      </form>
      <button onClick={goToSignup} className="btn btn-custom">회원가입</button>
    </div>
  );
};

export default Login;
