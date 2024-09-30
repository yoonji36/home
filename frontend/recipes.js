import React, { useEffect, useState } from 'react';
import axios from 'axios';

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
    <div>
      <h1>추천 레시피</h1>
      <ul>
        {recipes.map((recipe, index) => (
          <li key={index}>{recipe}</li>
        ))}
      </ul>
    </div>
  );
};

export default Recipes;
