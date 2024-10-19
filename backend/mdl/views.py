from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .gpt_api import res_recipe
from ultralytics import YOLO
import os
import pathlib
import torch
import json

# 경로 문제 해결 (PosixPath를 WindowsPath로 변경)
pathlib.PosixPath = pathlib.WindowsPath

# YOLOv5 모델 로드
model = torch.hub.load(
    repo_or_dir='C:/home/home/backend/yolov5',
    model='custom',
    path='C:/home/best.pt',
    source='local',
    force_reload=True
)

CLASS_NAME_MAPPING = {
    'eggplant': '가지',
    'potato': '감자',
    'sweet_potato': '고구마',
    'mackerel': '고등어',
    'egg': '달걀',
    'Bean sprouts' : '콩나물',
    'almond' : '아몬드',
    'apple' : '사과',
    'beef' : '소고기',
    'beet' : '비트',
    'bell_pepper' : '파프리카',
    'brocoli' : '브로콜리',
    'cabbage' : '양배추',
    'carrot' : '당근',
    'chicken_breast' : '닭가슴살',
    'chicken_leg' : '닭다리',
    'chicken_quarter' : '닭 1/4조각',
    'chicken_thigh' : '닭 넓적다리',
    'chicken_wing' : '닭날개',
    'cucumber' : '오이',
    'garlic' : '마늘',
    'green_onion' : '파',
    'mackerel' : '고등어',
    'onion' : '양파',
    'pork' : '돼지고기',
    'pork_belly' : '삼겹살',
    'potato' : '감자',
    'shirimp' : '새우',
    'spinach' : '시금치',
    'sweet_potato' : '고구마',
    'tofu' : '두부',
    'tomato' : '토마토',
    'zucchini' : '주키니'
}

@csrf_exempt
def image_upload(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # 이미지 저장
        uploaded_file = request.FILES['image']
        image_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))

        # 이미지 경로를 포함한 URL로 리다이렉트
        return redirect('process_image', image_path=image_path)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def process_image(request, image_path):
    # 이미지 경로 설정 및 분석
    full_image_path = os.path.join(default_storage.location, image_path)
    results = model(full_image_path)

    # 영어 이름을 한국어로 변환
    ingredients = results.pandas().xyxy[0]['name'].unique().tolist()
    translated_ingredients = [
        CLASS_NAME_MAPPING.get(name, name) for name in ingredients
    ]

    # 번역된 식재료를 템플릿으로 전달
    return render(request, 'ingredients.html', {'ingredients': translated_ingredients})


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
def generate_recipe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 클라이언트에서 보낸 데이터 파싱
            calorie_limit = data.get('calorie', 500)  # 기본 칼로리 제한 500
            ingredients = data.get('ingredients', [])  # 재료 리스트

            # GPT API 호출
            recipe_data = res_recipe(calorie_limit, ingredients)
            return JsonResponse({"recipe": recipe_data}, status=200)  # 성공 시 JSON 반환
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  # 오류 시 JSON 반환
    return JsonResponse({"error": "Invalid request method"}, status=405)


def recipes_page(request):
    return render(request, 'recipes.html')