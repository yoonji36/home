const MealPlanSetup = () => {
    const [weight, setWeight] = useState('');
    const [height, setHeight] = useState('');
    const [bmi, setBMI] = useState(null);
    const [dailyCalories, setDailyCalories] = useState(null);
  
    const handleCalculate = () => {
      const bmiValue = calculateBMI(weight, height / 100);
      const calorieValue = calculateDailyCalories('female', weight, height, 25);  // 나이는 임의로 25 설정
      setBMI(bmiValue);
      setDailyCalories(calorieValue);
    };
  
    return (
      <div>
        <h2>식단 맞춤 설정</h2>
        <input
          type="number"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
          placeholder="몸무게 (kg)"
        />
        <input
          type="number"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
          placeholder="키 (cm)"
        />
        <button onClick={handleCalculate}>BMI 및 칼로리 계산</button>
  
        {bmi && <p>당신의 BMI: {bmi}</p>}
        {dailyCalories && <p>일일 섭취 칼로리: {dailyCalories} kcal</p>}
      </div>
    );
  };
  