import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navigate } from 'react-router-dom';
import ImageUpload from './image-upload';
import Ingredients from './ingredients';
import Login from './login';
import Signup from './signup';
import HomePage from './HomePage'; // 홈 화면을 위한 컴포넌트
import PrivateRoute from './PrivateRoute'; // PrivateRoute 컴포넌트 import

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Navigate to ="/login" />} /> {/* 기본 URL이 로그인 페이지로 */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/image-upload" element={<PrivateRoute isAuthenticated={true} component={<ImageUpload />} />} />
        <Route path="/ingredients" element={<PrivateRoute isAuthenticated={true} component={<Ingredients />} />} />
        <Route path="/main" element={<PrivateRoute isAuthenticated={true} component={<HomePage />} />} />
      </Routes>
    </Router>
  );
}

export default App;
