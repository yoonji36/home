from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Profile
from django.views.generic import TemplateView
import json

# 메인 페이지를 렌더링하는 WelcomeView
class WelcomeView(TemplateView):
    template_name = 'welcome.html'  # 렌더링할 HTML 템플릿 지정

# 로그인 API
@csrf_exempt
def login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': '로그인 성공', 'redirect_url': '/homepage/'})
        else:
            return JsonResponse({'success': False, 'message': '로그인 실패'}, status=401)

    return JsonResponse({'error': '허용되지 않은 메서드입니다.'}, status=405)

# 회원가입 API
@csrf_exempt
def signup_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        height = data.get('height')
        weight = data.get('weight')
        blood_pressure = data.get('bloodPressure')

        try:
            # 중복된 사용자 이름 확인
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': '이미 존재하는 사용자입니다.'}, status=400)

            # 사용자 생성
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # 사용자 Profile 생성 및 저장
            profile = Profile(user=user, height=height, weight=weight, blood_pressure=blood_pressure)
            profile.save()

            return JsonResponse({'success': True, 'message': '회원가입 성공', 'redirect_url': '/homepage/'})

        except IntegrityError:
            return JsonResponse({'success': False, 'message': '사용자 생성 중 오류가 발생했습니다.'}, status=400)

    return JsonResponse({'error': '허용되지 않은 메서드입니다.'}, status=405)