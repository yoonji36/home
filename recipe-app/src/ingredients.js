import React, { useState } from 'react'
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const Ingredients = () => {
  const location = useLocation();
  const [ingredients, setIngredients] = useState(location.state?.ingredients || []);
  const [newIngredient, setNewIngredient] = useState('');
  const [showInput, setShowInput] = useState(false);

  // 재료 추가 함수
  const addIngredient = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/add_ingredient/', {
        ingredient: newIngredient
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.data.success) {
        setIngredients([...ingredients, { name: newIngredient }]);
        setNewIngredient(''); // 입력 필드 초기화
        setShowInput(false);
      } else {
        console.error(response.data.error);
      }
    } catch (error) {
      console.error('Error adding ingredient:', error);
    }
  };

  // 선택한 재료 삭제 함수
  const deleteIngredients = async () => {
    const ingredientsToDelete = ingredients.filter((ingredient) => ingredient.selected).map((ingredient) => ingredient.name);
    try {
      const response = await axios.post('http://127.0.0.1:8000/delete_ingredient/', {
        ingredients: ingredientsToDelete
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.data.success) {
        setIngredients(ingredients.filter((ingredient) => !ingredient.selected));
      } else {
        console.error(response.data.error);
      }
    } catch (error) {
      console.error('Error deleting ingredient:', error);
    }
  };

  const toggleSelectIngredient = (index) => {
    const updatedIngredients = [...ingredients];
    updatedIngredients[index] = { ...updatedIngredients[index], selected: !updatedIngredients[index].selected };
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
                checked={ingredient.selected || false}
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
