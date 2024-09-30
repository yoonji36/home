<<<<<<< HEAD
# django rest-framework
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from ultralytics import YOLO
from rest_framework import generics
from .models import Recipe
from .serializers import RecipeSerializer
import requests
=======
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
>>>>>>> 5dce980497d8ab786192f2bbd4b21caac0025649
import json
import pathlib
import torch  # YOLOv5 사용
import os

<<<<<<< HEAD
### YOLOv5 MODEL ###
# 임시로 PosixPath를 WindowsPath로 변경
pathlib.PosixPath = pathlib.WindowsPath

# YOLOv5 모델 로드 (torch.hub 사용)
model = torch.hub.load('C:/home/backend/yolov5', 'custom', path='C:/home/best.pt', source='local', force_reload=True)

# 이미지 업로드 VIEW
class ImageUploadView(APIView):
    def post(self, request, format=None):
        # 이미지 파일 가져오기
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 이미지 저장
        file_name = default_storage.save(image_file.name, image_file)
        image_path = default_storage.path(file_name)
        logging.info(f"Image saved at: {image_path}")

        # YOLOv5 모델을 이용해 객체 인식 수행
        try:
            # full_image_path는 Django의 파일 시스템에서 저장된 이미지의 전체 경로입니다.
            full_image_path = os.path.join(default_storage.location, file_name)
            
            # YOLOv5 모델로 이미지 처리
            results = model(full_image_path)
            
            # 인식된 객체(식재료) 이름 추출
            ingredients = results.pandas().xyxy[0]['name'].unique().tolist()

            # 식재료 리스트를 응답으로 반환
            return Response({"ingredients": ingredients}, status=status.HTTP_200_OK)
        
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            return Response({"error": "Error processing image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 재료 추가 및 삭제에 관한 API 뷰
@csrf_exempt  # 이 데코레이터는 Ajax POST 요청을 처리하기 위한 것임
@api_view(['POST'])
def add_ingredient(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_ingredient = data.get('ingredient')

            if new_ingredient:
                # 재료를 저장하는 로직을 여기에 추가
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid input'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt  # CSRF 보호 비활성화 (Ajax 요청에서 필요)
@api_view(['POST'])
def delete_ingredient(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ingredients_to_delete = data.get('ingredients', [])

            if ingredients_to_delete:
                # 재료를 삭제하는 로직을 여기에 추가
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid input'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# 레시피 목록 VIEW
@api_view(['GET'])
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
        return Response({'recipes': recipes}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 레시피 상세 VIEW
class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_object(self):
        recipe_id = self.kwargs['recipe_id']
        return self.queryset.filter(id=recipe_id).first()
    
    def get(self, request, recipe_id, *args, **kwargs):
        recipe = self.get_object()
        if recipe:
            recipe_data = self.serializer_class(recipe).data
            recipe_data['image_url'] = f'/static/images/{recipe_data.get("image", "default.jpg")}'
            return render(request, 'recipe_detail.html', {'recipe': recipe_data})
        else:
            return render(request, '404.html')
=======
# 임시로 PosixPath를 WindowsPath로 변경
pathlib.PosixPath = pathlib.WindowsPath

# YOLOv5 모델 로드 (torch.hub 사용) # ★★★★★
model = torch.hub.load('C:/Users/admin/hero/heroproj2024/backend/yolov5/', 'custom', path='C:/Users/admin/hero/heroproj2024/backend/best.pt', source='local', force_reload=True)  # ★★★★★

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
>>>>>>> 5dce980497d8ab786192f2bbd4b21caac0025649
