from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
from rest_framework import generics
from .models import Recipe
from .serializers import RecipeSerializer
from django.http import JsonResponse
import requests
import json
import pathlib
import torch  # YOLOv5 사용
import os

# 임시로 PosixPath를 WindowsPath로 변경
pathlib.PosixPath = pathlib.WindowsPath

# YOLOv5 모델 로드 (torch.hub 사용) # ★★★★★
model = torch.hub.load('C:/home/backend/yolov5', 'custom', path='C:/home/best.pt', source='local', force_reload=True)  # ★★★★★

def process_image(request, image_path):
    # YOLOv5 모델을 이용한 객체 인식
    full_image_path = os.path.join(default_storage.location, image_path)
    results = model(full_image_path)
    ingredients = results.pandas().xyxy[0]['name'].unique().tolist()  # 인식된 객체 이름 추출

    # ingredients.html로 식재료 리스트 전달
    return render(request, 'ingredients.html', {'ingredients': ingredients})


@csrf_exempt  # 이 데코레이터는 Ajax POST 요청을 처리하기 위한 것임
def add_ingredient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_ingredient = data.get('ingredient')

        if new_ingredient:
            # 재료를 저장하는 로직을 여기에 추가
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid input'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt  # CSRF 보호 비활성화 (Ajax 요청에서 필요)
def delete_ingredient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ingredients_to_delete = data.get('ingredients', [])

        if ingredients_to_delete:
            # 재료를 삭제하는 로직을 여기에 추가
            # 예를 들어, DB에서 해당 재료들을 삭제하는 코드를 작성
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid input'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def recipe_list(request):
    try:
        api_key = '71ea164165cc493aa7f6'
        service_id = 'COOKRCP01'
        data_type = 'json'  # 'json' 형식을 명시적으로 설정
        start_idx = 1
        end_idx = 10

        url = f'http://openapi.foodsafetykorea.go.kr/api/{api_key}/{service_id}/{data_type}/{start_idx}/{end_idx}'
        response = requests.get(url)
        data = response.json()  # XML이 아닌 JSON을 사용하여 응답을 가져옴

        # 필요한 데이터만 추출하여 반환
        recipes = data.get('COOKRCP01', {}).get('row', [])
        return JsonResponse({'recipes': recipes}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def recipe_detail(request, recipe_id):
    recipe = RECIPES.get(recipe_id)
    if recipe:
        # 예외 처리: 만약 'image' 키가 없다면 기본값을 사용
        recipe['image_url'] = f'/static/images/{recipe.get("image", "default.jpg")}'
        return render(request, 'recipe_detail.html', {'recipe': recipe})
    else:
        return render(request, '404.html')