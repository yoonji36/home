async function recognizeIngredients() {
    const formData = new FormData();
    const image = document.getElementById('imageUpload').files[0];
    formData.append('image', image);

    const response = await fetch('http://localhost:8000/api/recognize-ingredients', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    if (data.error) {
        document.getElementById('errorMessage').innerText = "적합하지 않은 사진입니다.";
    } else {
        window.location.href = "ingredients.html";
    }
}
