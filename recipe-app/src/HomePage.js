import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './HomePage.css'; // HomePage.css 파일을 import

const HomePage = () => {
  const [userId, setUserId] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // 로그인 후 사용자 ID를 localStorage에 저장했다고 가정하고 가져옴
    const storedUserId = localStorage.getItem('userId');
    if (storedUserId) {
      setUserId(storedUserId);
    } else {
      // 사용자 ID가 없으면 로그인 페이지로 이동
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = () => {
    // 로그아웃 시 localStorage에서 사용자 정보 삭제 후 로그인 페이지로 이동
    localStorage.removeItem('userId');
    navigate('/login');
  };

  const handleMyProfile = () => {
    navigate('');
  };

  const handleRecipeCreate = () => {
    navigate('/image-upload');
  };

  return (
    <div className="body">
      {/* 메인 섹션 상단 */}
      <div className="container header-section">
        {/* 사용자 환영 메시지 */}
        <div className="welcome-text">
          <span>{userId} 님, 환영합니다!</span>
          <div className="buttons">
            <button onClick={handleMyProfile} className="button">나의 기록</button>
            <button onClick={handleLogout} className="button logout-button">로그아웃</button>
          </div>
        </div>

        {/* 레시피 만들기 버튼 */}
        <button onClick={handleRecipeCreate} className="recipe-button">레시피 만들기</button>
      </div>

      {/* 메인 콘텐츠 */}
      <div className="container main-content">
        {/* 신규 글 카드 */}
        <div className="card card-custom">
          <div className="card-body">
            <h5 className="card-title">신규 글</h5>
            <p className="card-text">여기에 신규 글 내용을 추가합니다. 최신 글이 이곳에 표시됩니다.</p>
          </div>
        </div>

        {/* 당첨자 뉴스 카드 */}
        <div className="card card-custom">
          <div className="card-body">
            <h5 className="card-title">당첨자 뉴스</h5>
            <p className="card-text">당첨자 관련 뉴스는 여기에 표시됩니다. 최신 정보를 업데이트하세요.</p>
          </div>
        </div>
      </div>

      <footer>
        <p>© 2024 혈당히어로 gotchA! 당뇨병 건강관리 헬스케어 웹사이트 제작</p>
        <p>all rights reserved.</p>
      </footer>
    </div>
  );
};

export default HomePage;
