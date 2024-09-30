# backend/app/views.py

from django.shortcuts import render
<<<<<<< HEAD

=======
import sys
>>>>>>> 5dce980497d8ab786192f2bbd4b21caac0025649
import torch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Ingredient
from PIL import Image

<<<<<<< HEAD
=======
sys.path.append('C:/Users/admin/hero/heroproj2024/backend/yolov5')
model = torch.hub.load('C:/Users/admin/hero/heroproj2024/backend/yolov5', 'custom', path='C:/Users/admin/hero/heroproj2024/backend/yolov5/best.pt')
>>>>>>> 5dce980497d8ab786192f2bbd4b21caac0025649
@csrf_exempt
def recognize_ingredients(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if not image:
            return JsonResponse({"error": "No image provided"}, status=400)

        # YOLOv5 모델 로드 및 이미지 처리
        img = Image.open(image)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
        results = model(img)
        ingredients = results.pandas().xyxy[0]['name'].tolist()

        if not ingredients:
            return JsonResponse({"error": "No ingredients detected"}, status=400)

        # 인식된 재료를 데이터베이스에 저장
        for ingredient_name in ingredients:
            Ingredient.objects.get_or_create(name=ingredient_name)

        return JsonResponse({"ingredients": ingredients})

    return JsonResponse({"error": "Invalid request method"}, status=405)