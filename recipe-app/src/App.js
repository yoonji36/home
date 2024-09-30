import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ImageUpload from './image-upload';
import Ingredients from './ingredients';
import Login from './login';
import Signup from './Signup';
import HomePage from './HomePage'; // 홈 화면을 위한 컴포넌트
import PrivateRoute from './PrivateRoute'; // PrivateRoute 컴포넌트 import

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/image-upload" element={<PrivateRoute isAuthenticated={true} component={<ImageUpload />} />} />
        <Route path="/ingredients" element={<PrivateRoute isAuthenticated={true} component={<Ingredients />} />} />
        <Route path="/home" element={<PrivateRoute isAuthenticated={true} component={<HomePage />} />} />
        <Route path="/" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
