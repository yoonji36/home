from django.shortcuts import render
from .models import Recipe
from django.http import JsonResponse
import requests

# api
def fetch_recipes():
    api_key = 'your_api_key'
    service_id = 'COOKRCP01'  # 레시피 서비스 ID
    data_type = 'json'
    start_idx = 1
    end_idx = 100  # 100개의 레시피를 가져옴

    url = f'http://openapi.foodsafetykorea.go.kr/api/{api_key}/{service_id}/{data_type}/{start_idx}/{end_idx}'
    
    response = requests.get(url)
    recipes_data = response.json().get('COOKRCP01', {}).get('row', [])
    
    return recipes_data  # 레시피 데이터 반환


# 레시피 데이터 DB에 저장 (중복 확인)
def save_recipes_to_db():
    recipes_data = fetch_recipes()  # API 호출로 레시피 데이터 가져오기
    
    for recipe_data in recipes_data:
        # 레시피 데이터 DB에 저장 (중복 확인)
        Recipe.objects.get_or_create(
            name=recipe_data['RCP_NM'],
            image_url=recipe_data['ATT_FILE_NO_MAIN'],
            ingredients=recipe_data['RCP_PARTS_DTLS'],
            cooking_steps="\n".join([recipe_data.get(f'MANUAL{i:02d}', '') for i in range(1, 21)]),  # MANUAL01~20 단계 합침
            nutrition_info=f"열량: {recipe_data.get('INFO_ENG', '')}kcal, 탄수화물: {recipe_data.get('INFO_CAR', '')}g, 단백질: {recipe_data.get('INFO_PRO', '')}g"
        )

# 레시피 데이터 조회 및 표시
def get_all_recipes(request):
    recipes = Recipe.objects.all().values('name', 'image_url', 'ingredients', 'cooking_steps', 'nutrition_info')
    return JsonResponse({'recipes': list(recipes)})
