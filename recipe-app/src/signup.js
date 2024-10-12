import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // useNavigate import
import 'bootstrap/dist/css/bootstrap.min.css';
import './signup.css'; // Signup.css 파일을 따로 작성하고 사용할 경우

// axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',  // Django 서버 주소
  withCredentials: true,
});

const Signup = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    height: '',
    weight: '',
    bloodPressure: '',
  });

  const [errors, setErrors] = useState({});
  const [csrfToken, setCsrfToken] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCSRFToken = async () => {
      try {
        const response = await axiosInstance.get('/login/csrf_token_view/');
        setCsrfToken(response.data.csrfToken);
      } catch (error) {
        console.error('CSRF 토큰을 가져오는 데 실패했습니다:', error);
      }
    };
    fetchCSRFToken();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const validate = () => {
    const newErrors = {};
    // 사용자 ID 유효성 검사
    if (!formData.username) {
      newErrors.username = '사용자 ID를 입력해주세요.';
    }
    // 비밀번호 유효성 검사
    if (!formData.password) {
      newErrors.password = '비밀번호를 입력해주세요.';
    } else if (formData.password.length < 6) {
      newErrors.password = '비밀번호는 최소 6자 이상이어야 합니다.';
    }
    // 키 유효성 검사 (숫자인지 확인)
    if (!formData.height || isNaN(formData.height)) {
      newErrors.height = '유효한 키(cm)를 입력해주세요.';
    }
    // 몸무게 유효성 검사 (숫자인지 확인)
    if (!formData.weight || isNaN(formData.weight)) {
      newErrors.weight = '유효한 몸무게(kg)를 입력해주세요.';
    }
    // 혈압 유효성 검사 (숫자인지 확인)
    if (!formData.bloodPressure || isNaN(formData.bloodPressure)) {
      newErrors.bloodPressure = '유효한 혈압 값을 입력해주세요.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // 입력값 유효성 검사
    if (!validate()) return;

    // CSRF 토큰 가져오기
    try {
      console.log("Sending data:", formData);
      console.log("CSRF Token:", csrfToken);
      const response = await axiosInstance.post('/login/signup/', {
        username: formData.username,
        password: formData.password,
        height: parseFloat(formData.height),
        weight: parseFloat(formData.weight),
        bloodPressure: formData.bloodPressure,
      }, {
        headers: {
          'X-CSRFToken': csrfToken,
        },
      });

      console.log("Response received:", response);

      // 로그: 요청 보내기 직전
      console.log("Sending POST request to /login/signup/ with headers:", {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      });

      // 로그: 요청 성공 시 응답 확인
      console.log("Response received:", response);
  
      if (response.data.success) {
        console.log('회원 가입 성공:', response.data);
        alert('회원 가입에 성공하였습니다.');
        navigate('/main/');
      } else {
        console.error('회원 가입 실패:', response.data.message);
        alert(response.data.message);
      }
    } catch (error) {
      console.error('회원 가입 오류:', error);
      if (error.response) {
        console.error('응답 데이터:', error.response.data);
        console.error('응답 상태:', error.response.status);
        console.error('응답 헤더:', error.response.headers);
        alert(`회원 가입 실패: ${error.response.data.message}`);
      } else if (error.request) {
        console.error('요청 정보:', error.request);
        alert('서버에 연결할 수 없습니다. 네트워크 연결을 확인하세요.');
      } else {
        console.error('에러 메시지:', error.message);
        alert('회원 가입 중 오류가 발생하였습니다. 나중에 다시 시도해주세요.');
      }
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
          {errors.username && <div className="text-danger">{errors.username}</div>}
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
          {errors.password && <div className="text-danger">{errors.password}</div>}
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
          {errors.height && <div className="text-danger">{errors.height}</div>}
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
          {errors.weight && <div className="text-danger">{errors.weight}</div>}
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
          {errors.bloodPressure && <div className="text-danger">{errors.bloodPressure}</div>}
        </div>

        <button type="submit" className="btn btn-custom">회원 가입</button>
      </form>
    </div>
  );
};

export default Signup;
