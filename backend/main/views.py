<<<<<<< HEAD
# django rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage  # default_storage 임포트
from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.cache import cache
from django.http import JsonResponse
import requests, os, logging

logger = logging.getLogger(__name__)

class WelcomeView(APIView):
    def get(self, request):
        user_id = request.user.id if request.user.is_authenticated else 'Guest'
        return Response({'message': f'Welcome, {user_id}!'}, status=status.HTTP_200_OK)
=======
from django.shortcuts import render
from django.http import JsonResponse
import openai

# OpenAI API 키 설정
openai.api_key = 'your-openai-api-key'

# OpenAI를 이용한 맞춤형 식단 생성 함수
def generate_meal_plan(bmi, target_calories, blood_sugar):
    prompt = f"""
    사용자 정보: BMI는 {bmi}, 하루 섭취 칼로리 목표는 {target_calories} kcal입니다.
    혈당 수치는 {blood_sugar}이며, Glycemic Index(GI)가 55 이하인 음식으로 아침, 점심, 저녁 식단을 만들어 주세요.
    각각의 식단은 칼로리 목표에 맞춰 주세요.
    """
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=300
    )
    
    return response.choices[0].text.strip()

# 맞춤형 식단 생성 API
def get_meal_plan(request):
    bmi = request.GET.get('bmi')
    target_calories = request.GET.get('calories')
    blood_sugar = request.GET.get('blood_sugar')

    meal_plan = generate_meal_plan(bmi, target_calories, blood_sugar)

    return JsonResponse({'meal_plan': meal_plan})
>>>>>>> 5dce980497d8ab786192f2bbd4b21caac0025649
