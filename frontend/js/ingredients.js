async function fetchIngredients() {
    const response = await fetch('http://localhost:8000/api/get-ingredients');
    const data = await response.json();
    const ingredientsList = document.getElementById('ingredientsList');

    data.ingredients.forEach(ingredient => {
        const li = document.createElement('li');
        li.textContent = ingredient;
        ingredientsList.appendChild(li);
    });
}

async function addIngredient() {
    const newIngredient = document.getElementById('newIngredient').value;
    await fetch('http://localhost:8000/api/add-ingredient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newIngredient })
    });
    window.location.reload();
}

function nextPage() {
    window.location.href = "final_ingredients.html";
}

fetchIngredients();
