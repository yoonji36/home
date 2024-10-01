import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

const Ingredients = () => {
  const location = useLocation();
  const [ingredients, setIngredients] = useState(location.state?.ingredients || []);
  const [newIngredient, setNewIngredient] = useState('');
  
  // 추가: 사용자 입력 상태 (BMI, 칼로리 목표, 혈당 수치)
  const [bmi, setBmi] = useState('');
  const [calories, setCalories] = useState('');
  const [bloodSugar, setBloodSugar] = useState('');
  const [mealPlan, setMealPlan] = useState('');

  // 재료 추가 함수
  const addIngredient = async () => {
    try {
      const response = await axios.post('/api/add_ingredient/', { ingredient: newIngredient });

      if (response.data.success) {
        setIngredients([...ingredients, newIngredient]);
        setNewIngredient('');
      }
    } catch (error) {
      console.error('Error adding ingredient:', error);
    }
  };

  // 재료 삭제 함수
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

  // 선택 토글 함수
  const toggleSelectIngredient = (index) => {
    const updatedIngredients = [...ingredients];
    updatedIngredients[index].selected = !updatedIngredients[index].selected;
    setIngredients(updatedIngredients);
  };

  // 추가: 맞춤형 식단 생성 API 호출 함수
  const generateMealPlan = async () => {
    try {
      const response = await axios.get(`/api/get-meal-plan`, {
        params: {
          bmi,
          calories,
          blood_sugar: bloodSugar,
        },
      });

      if (response.data) {
        setMealPlan(response.data.meal_plan);  // 받아온 식단을 상태에 저장
      }
    } catch (error) {
      console.error('Error generating meal plan:', error);
    }
  };

  return (
    <div className="container">
      <h1>재료 리스트</h1>
      <ul>
        {ingredients.map((ingredient, index) => (
          <li key={index}>
            <input type="checkbox" onChange={() => toggleSelectIngredient(index)} />
            {ingredient}
          </li>
        ))}
      </ul>
      <button onClick={deleteIngredients}>삭제</button>

      <div>
        <input
          type="text"
          value={newIngredient}
          onChange={(e) => setNewIngredient(e.target.value)}
          placeholder="재료를 입력하세요"
        />
        <button onClick={addIngredient}>재료 추가</button>
      </div>

      {/* 추가: BMI, 칼로리 목표, 혈당 수치 입력 */}
      <div>
        <h2>맞춤형 식단 생성</h2>
        <label>BMI:</label>
        <input
          type="number"
          value={bmi}
          onChange={(e) => setBmi(e.target.value)}
          placeholder="BMI 입력"
        />
        <label>칼로리 목표:</label>
        <input
          type="number"
          value={calories}
          onChange={(e) => setCalories(e.target.value)}
          placeholder="칼로리 목표 입력"
        />
        <label>혈당 수치:</label>
        <input
          type="number"
          value={bloodSugar}
          onChange={(e) => setBloodSugar(e.target.value)}
          placeholder="혈당 수치 입력"
        />
        <button onClick={generateMealPlan}>식단 생성</button>
      </div>

      {/* 추가: 생성된 식단을 화면에 표시 */}
      {mealPlan && (
        <div>
          <h3>생성된 맞춤형 식단</h3>
          <p>{mealPlan}</p>
        </div>
      )}
    </div>
  );
};

export default Ingredients;