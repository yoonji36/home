from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile  # Profile 모델 임포트
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError  # 추가: 중복 발생 시 예외 처리용
import json

# 로그인 페이지 렌더링
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 사용자 인증 처리
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main-page')  # 로그인 성공 시 메인 페이지로 리다이렉트
        else:
            return render(request, 'login.html', {'error': '로그인 실패'})  # 실패 시 에러 메시지

    return render(request, 'login.html')

# 회원 가입 페이지 렌더링 및 회원 가입 처리
def signup_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        blood_pressure = request.POST.get('bloodPressure')

        try:
            # 사용자 생성
            user = User.objects.create_user(username=username, password=password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) # 자동 로그인
                return redirect('main-page') # 메인 페이지로 리다이렉트
            
            else:
                messages.error(request, '회원가입에 실패했습니다')

            # 중복된 사용자 이름 확인 및 예외 처리
            if User.objects.filter(username=username).exists():
                messages.error(request, '이미 존재하는 사용자 이름입니다')
                # return render(request, 'signup.html', {'error': '이미 존재하는 사용자입니다.'})  # 중복 사용자 처리

            # 사용자 Profile 생성 및 저장
            profile = Profile(user=user, height=height, weight=weight, blood_pressure=blood_pressure)
            profile.save()

        except IntegrityError:  # 데이터베이스 제약 조건 위반 시 예외 처리
            return render(request, 'signup.html', {'error': '사용자 생성 중 오류가 발생했습니다.'})

    return render(request, 'signup.html')