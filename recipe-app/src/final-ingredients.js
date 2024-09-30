import React from 'react';

const FinalIngredientsList = () => {
    const generateRecipes = () => {
        // 레시피 생성 로직을 여기에 작성
        alert("레시피 생성 기능을 구현하세요.");
    };

    return (
        <div>
            <header>
                <h1>최종 재료 리스트</h1>
            </header>
            <main>
                <ul id="finalIngredientsList"></ul>
                <button onClick={generateRecipes}>레시피 생성</button>
            </main>
        </div>
    );
};

export default FinalIngredientsList;
