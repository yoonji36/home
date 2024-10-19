from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile  # Profile 모델 임포트
from django.db import IntegrityError

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

    return render(request, 'login.html')  # frontend/login.html 사용

# 회원가입 페이지 렌더링 및 회원가입 처리
def signup_page(request):
    if request.method == "POST":
        # POST 데이터 가져오기 (오타나 누락 방지)
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        height = request.POST.get('height', '').strip()
        weight = request.POST.get('weight', '').strip()
        blood_pressure = request.POST.get('blood_pressure', '').strip()

        # 사용자 이름 중복 확인
        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 존재하는 사용자 이름입니다.')
            return render(request, 'signup.html')

        try:
            # 사용자 생성
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # 자동 로그인 처리
            login(request, user)  # 인증 없이 바로 로그인

            # BMI 계산 및 프로필 생성
            h2 = float(height) / 100.0  # 키를 미터로 변환
            bmi = int(int(weight) / (h2 * h2))  # BMI 계산

            # 새 Profile 객체 생성
            profile = Profile.objects.create(
                user=user,
                height=height,
                weight=weight,
                bmi=bmi,
                blood_pressure=blood_pressure
            )
            profile.save()  # 프로필 저장

            return redirect('/main/')  # 메인 페이지로 리다이렉트

        except ValueError as e:  # BMI 계산 오류 등 예외 처리
            messages.error(request, f'입력값 오류가 발생했습니다: {str(e)}')
            return render(request, 'signup.html', {'error': '프로필 생성 실패'})

        except IntegrityError:  # 데이터베이스 제약 조건 위반 예외 처리
            return render(request, 'signup.html', {'error': '사용자 생성 중 오류가 발생했습니다.'})

        except Exception as e:  # 기타 예상치 못한 예외 처리
            messages.error(request, f'예기치 못한 오류가 발생했습니다: {str(e)}')
            return render(request, 'signup.html', {'error': '회원가입 실패'})

    return render(request, 'signup.html')  # 회원가입 페이지 렌더링