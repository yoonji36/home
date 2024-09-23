import React from 'react';
import { useNavigate } from 'react-router-dom';

const ErrorPage = () => {
  const navigate = useNavigate();

  const goBack = () => {
    navigate('/image-upload');
  };

  const retry = () => {
    navigate('/ingredients');
  };

  return (
    <div>
      <h1>적합하지 않은 사진입니다.</h1>
      <button onClick={goBack}>이미지 업로드로 돌아가기</button>
    </div>
  );
};

export default ErrorPage;
