function fetchRecipes() {
    // URL에서 레시피 데이터를 쿼리 파라미터로 가져오기
    const urlParams = new URLSearchParams(window.location.search);
    const result = urlParams.get('result'); // 쿼리 파라미터의 'result' 값

    // 레시피 목록을 가져올 HTML 요소
    const recipesList = document.getElementById("recipesList");

    if (result) {
        // 쿼리 파라미터 값이 있으면 쉼표로 구분된 레시피 리스트를 배열로 변환
        const recipes = result.split(',');

        // 각 레시피를 리스트 아이템으로 추가
        recipes.forEach(recipe => {
            const li = document.createElement('li');
            li.textContent = recipe;  // 각 레시피 이름을 리스트 아이템으로 추가
            recipesList.appendChild(li);
        });
    } else {
        // 레시피 결과가 없을 경우 메시지 출력
        const noRecipes = document.createElement('p');
        noRecipes.textContent = "추천할 레시피가 없습니다.";
        recipesList.appendChild(noRecipes);
    }
}

// 페이지가 로드되면 fetchRecipes 함수를 실행
window.onload = fetchRecipes;
