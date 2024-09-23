import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './recipes.css';  // 기존 CSS 파일 임포트

const Recipes = () => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await axios.get('/api/generate-recipes/');
        setRecipes(response.data.recipes);
      } catch (error) {
        console.error('Error fetching recipes:', error);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <div className="recipes-container">
      <h1>추천 레시피</h1>
      <ul>
        {recipes.map((recipe, index) => (
          <li key={index}>
            <a href="#">
              <div>
                <img src={`path/to/image/${recipe.image}`} alt={`Recipe ${index + 1}`} />
                <span>{recipe.name}</span>
              </div>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Recipes;
