from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
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

def recipe_list(request):
    # 필요시 데이터를 여기서 처리하고 템플릿에 전달할 수 있습니다.
    return render(request, 'recipe_list.html')

RECIPES = {
    1: {
        'title': '계란 토마토 당근 볶음',
        'ingredients': ['계란 2개', '토마토 1개', '당근 1/2개', '양파 1/4개 (선택 사항)', '소금, 후추, 올리브 오일'],
        'instructions': '''1. 당근과 양파를 얇게 썰어 준비합니다.
                            2. 토마토는 먹기 좋은 크기로 썰어둡니다.
                            3. 팬에 올리브 오일을 두르고 당근과 양파를 볶다가, 어느 정도 익으면 토마토를 넣고 볶습니다.
                            4. 계란을 잘 풀어서 소금, 후추로 간을 한 후 팬에 부어 다른 재료와 함께 볶습니다.
                            5. 모든 재료가 익으면 불을 끄고 그릇에 담아 완성합니다.''',
        'image': 'recipe01.jpg',  # 이미지 경로 추가
        'image_url': '/static/images/recipe01.jpg',  # 이미지 경로
    },
    2: {
        'title': '계란 토마토 당근 스크램블',
        'ingredients': ['계란 3개', '토마토 1개', '당근 1/4개', '우유 2큰술 (선택 사항)', '소금, 후추, 올리브 오일'],
        'instructions': '''1. 계란을 그릇에 넣고 우유를 첨가한 후 잘 섞어줍니다.
                            2. 토마토와 당근을 작게 다집니다.
                            3. 팬에 올리브 오일을 두르고 당근을 먼저 볶은 후 토마토를 넣고 살짝 볶습니다.
                            4. 그 위에 계란물을 부어 스크램블 하듯 저어줍니다.
                            5. 소금과 후추로 간을 맞추고 접시에 담아 완성합니다.''',
        'image': 'recipe02.jpg',  # 이미지 경로 추가
        'image_url': '/static/images/recipe02.jpg',  # 이미지 경로
    },
    3: {
        'title': '계란 토마토 당근 오믈렛',
        'ingredients': ['계란 2개', '토마토 1개', '당근 1/4개', '치즈 (선택 사항)', '소금, 후추, 올리브 오일'],
        'instructions': '''1. 토마토와 당근을 작게 썰어 준비합니다.
                            2. 계란을 잘 풀어 소금과 후추로 간을 합니다.
                            3. 팬에 올리브 오일을 두르고 토마토와 당근을 살짝 볶은 후, 계란물을 부어줍니다.
                            4. 치즈를 계란 위에 올려줍니다.
                            5. 계란이 반쯤 익으면 반으로 접어 오믈렛 모양을 만듭니다.
                            6. 약한 불에서 익혀 완성합니다.''',
        'image': 'recipe03.jpg',  # 이미지 경로 추가
        'image_url': '/static/images/recipe03.jpg',  # 이미지 경로
    }
}

def recipe_list(request):
    return render(request, 'recipe_list.html')

def recipe_detail(request, recipe_id):
    recipe = RECIPES.get(recipe_id)
    if recipe:
        # 예외 처리: 만약 'image' 키가 없다면 기본값을 사용
        recipe['image_url'] = f'/static/images/{recipe.get("image", "default.jpg")}'
        return render(request, 'recipe_detail.html', {'recipe': recipe})
    else:
        return render(request, '404.html')
    
