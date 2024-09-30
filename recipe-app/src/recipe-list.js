import React, { useEffect, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './recipe-list.css';

const RecipeList = () => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        // Django API에서 데이터 가져오기
        const response = await axios.get('/mdl/recipe_list'); // Django API 엔드포인트
        setRecipes(response.data.recipes); // 응답에서 recipes 배열을 추출하여 상태로 설정
      } catch (error) {
        console.error('API 호출 오류:', error);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <div className="recipe-list">
      <h1>레시피 목록</h1>
      <div className="recipe-card-container">
        {recipes.length > 0 ? (
          recipes.map((recipe, index) => (
            <div key={index} className="recipe-card">
              {/* 레시피 제목 */}
              <h2>{recipe.RCP_NM}</h2>
              
              {/* 레시피 이미지 */}
              {recipe.ATT_FILE_NO_MAIN && (
                <img 
                  src={recipe.ATT_FILE_NO_MAIN} 
                  alt={recipe.RCP_NM} 
                  style={{ width: '200px', height: 'auto' }}
                />
              )}
            </div>
          ))
        ) : (
          <p>레시피를 불러오는 중입니다...</p>
        )}
      </div>
    </div>
  );
};

export default RecipeList;