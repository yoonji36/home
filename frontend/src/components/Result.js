import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const Results = () => {
  const { recipe_id } = useParams();
  const [recipe, setRecipe] = useState(null);

  useEffect(() => {
    fetch(`/get_recipe/${recipe_id}`)
      .then(response => response.json())
      .then(data => setRecipe(data));
  }, [recipe_id]);

  return (
    <div>
      <h1>Recipe Result</h1>
      {recipe ? (
        <div>
          <h2>Ingredients:</h2>
          <ul>
            {recipe.ingredients.map((ingredient, index) => (
              <li key={index}>{ingredient}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Loading recipe...</p>
      )}
    </div>
  );
};

export default Results;