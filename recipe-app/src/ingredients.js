import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './ingredients.css';

const Ingredients = () => {
  const location = useLocation();
  const [ingredients, setIngredients] = useState(location.state?.ingredients || []);
  const [newIngredient, setNewIngredient] = useState('');
  const [showInput, setShowInput] = useState(false);

  const addIngredient = async () => {
    try {
      const response = await axios.post('/api/add_ingredient/', { ingredient: newIngredient });

      if (response.data.success) {
        setIngredients([...ingredients, newIngredient]);
        setNewIngredient('');
        setShowInput(false);
      }
    } catch (error) {
      console.error('Error adding ingredient:', error);
    }
  };

  const deleteIngredients = async () => {
    const selectedIngredients = ingredients.filter((ingredient) => ingredient.selected);
    try {
      const response = await axios.post('/api/delete_ingredient/', { ingredients: selectedIngredients });

      if (response.data.success) {
        setIngredients(ingredients.filter((ingredient) => !ingredient.selected));
      }
    } catch (error) {
      console.error('Error deleting ingredients:', error);
    }
  };

  const toggleSelectIngredient = (index) => {
    const updatedIngredients = [...ingredients];
    updatedIngredients[index].selected = !updatedIngredients[index].selected;
    setIngredients(updatedIngredients);
  };

  return (
    <div className="container">
      <h1>재료 리스트</h1>
      <ul className="ingredient-list">
        {ingredients.map((ingredient, index) => (
          <li key={index} className="ingredient-item">
            <div>
              <input 
                type="checkbox" 
                className="ingredient-checkbox" 
                onChange={() => toggleSelectIngredient(index)} 
              />
              {ingredient.name}
            </div>
          </li>
        ))}
      </ul>
      <div className="text-center">
        <button onClick={deleteIngredients} className="btn btn-delete">삭제</button>
      </div>

      <div className="add-ingredient-section">
        <button onClick={() => setShowInput(true)} className="btn btn-custom">재료 추가</button>
        {showInput && (
          <div id="ingredient-input-container">
            <input
              type="text"
              value={newIngredient}
              onChange={(e) => setNewIngredient(e.target.value)}
              placeholder="재료를 입력하세요"
              className="form-control my-2"
            />
            <button onClick={addIngredient} className="btn btn-primary">추가하기</button>
          </div>
        )}
      </div>

      <button type="button" id="recipe-btn" className="btn btn-primary recipe-btn">
        레시피 만들기
      </button>
    </div>
  );
};

export default Ingredients;
