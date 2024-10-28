from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .gpt_api import res_recipe
from .models import Recipe
from ultralytics import YOLO
import os, pathlib, torch, json

# 경로 문제 해결 (PosixPath를 WindowsPath로 변경)
pathlib.PosixPath = pathlib.WindowsPath

# YOLOv5 모델 로드
model = torch.hub.load(
    repo_or_dir='C:/home/home/backend/yolov5',
    model='custom',
    path='C:/home/home/best.pt',
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

def upload_view(request):
    return render(request, 'image-upload.html')

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

# 레시피 생성
@csrf_exempt
def generate_recipe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            calorie_limit = data.get('calorie', 500)
            ingredients = data.get('ingredients', [])
            previous_title = data.get('previous_title')

            if not data.get('ingredients'):
                return JsonResponse({'error': '재료가 필요합니다.'}, status=400)

            # GPT API 호출 준비
            prompt = f"{', '.join(ingredients)}를 사용하여 {calorie_limit} 칼로리 이하의 세계적인 요리 레시피를 한국어로 추천해줘."
            if previous_title:
                prompt += f" 단, '{previous_title}'과 동일하지 않은 다른 장르의 레시피를 추천해줘"

            # GPT API 호출 및 응답 처리
            recipe_data = res_recipe(calorie_limit, ingredients, prompt)

            # 응답 데이터의 필수 키를 검증합니다.
            required_keys = {"title", "ingredients", "instructions"}
            if not required_keys.issubset(recipe_data.keys()):
                raise ValueError(f"응답에 필요한 키가 없습니다. 응답 키: {recipe_data.keys()}")

            # 세션에 레시피 저장
            request.session['recipe'] = recipe_data

            return JsonResponse({"recipe": recipe_data}, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"JSON 파싱 오류: {str(e)}"}, status=500)
        except ValueError as e:
            return JsonResponse({"error": f"응답 검증 오류: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"레시피 생성 오류: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# 레시피 생성 페이지 리다이렉트
def recipes_page(request):
    # 세션에서 레시피 데이터를 가져옴
    recipe_data = request.session.get('recipe')
    
    if not recipe_data:
        return redirect('upload_page')  # 레시피가 없으면 업로드 페이지로 이동

    return render(request, 'recipes.html', {'recipe': recipe_data})

# 레시피 재료 세션정보
def get_ingredients_from_session(request):
    # 세션에서 ingredients와 calorie_limit 가져오기
    ingredients = request.session.get('ingredients', [])
    calorie_limit = request.session.get('calorie_limit', 500)  # 기본값: 500

    return JsonResponse({
        'ingredients': ingredients,
        'calorieLimit': calorie_limit
    })

# 레시피 세션정보
def get_recipe_from_session(request):
    # 세션에서 저장된 레시피 데이터를 가져오는 함수
    recipe_data = request.session.get('recipe')
    if recipe_data:
        return JsonResponse({'recipe': recipe_data}, status=200)
    return JsonResponse({'error': '레시피 데이터가 없습니다.'}, status=404)

# 레시피 재료&칼로리 세션 저장
@csrf_exempt
def save_ingredients_and_calorie(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ingredients = data.get('ingredients', [])
            calorie_limit = data.get('calorie_limit', 500)

            # 재료와 칼로리 데이터를 세션에 저장
            request.session['ingredients'] = ingredients
            request.session['calorie_limit'] = calorie_limit

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# 레시피 저장
@csrf_exempt
@login_required  # 로그인된 사용자만 접근 가능하도록 설정
def save_recipe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        ingredients = data.get('ingredients')
        instructions = data.get('instructions')

        # 모든 필드가 존재하는지 확인
        if title and ingredients and instructions:
            Recipe.objects.create(
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                user=request.user  # 현재 로그인된 사용자 저장
            )
            return JsonResponse({'message': '레시피가 성공적으로 저장되었습니다!'}, status=201)
        else:
            return JsonResponse({'error': '필요한 레시피 정보가 부족합니다.'}, status=400)
    return JsonResponse({'error': '잘못된 요청 방식입니다.'}, status=405)