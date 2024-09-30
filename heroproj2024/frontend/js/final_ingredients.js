async function fetchFinalIngredients() {
    const response = await fetch('http://localhost:8000/api/get-ingredients');
    const data = await response.json();
    const finalList = document.getElementById("finalIngredientsList");

    data.ingredients.forEach(ingredient => {
        const li = document.createElement("li");
        li.textContent = ingredient;
        finalList.appendChild(li);
    });
}

async function generateRecipes() {
    const response = await fetch('http://localhost:8000/api/generate-recipes');
    const data = await response.json();
    window.location.href = `recipes.html?result=${data.recipes.join(",")}`;
}

fetchFinalIngredients();
