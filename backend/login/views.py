from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Profile
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
import json

# 로그인 페이지 렌더링 시 CSRF 쿠키 설정
@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({'message': 'CSRF 쿠키 설정 완료'}, status=200)

# 로그인 API
@csrf_exempt
def login_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': '로그인 성공', 'redirect_url': '/main/'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': '로그인 실패'}, status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '잘못된 요청 형식입니다.'}, status=400)

    return JsonResponse({'error': '허용되지 않은 메서드입니다.'}, status=405)

# 회원가입 API
@csrf_exempt
def signup_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # 서버 콘솔에서 데이터 확인
            username = data.get('username')
            password = data.get('password')
            height = data.get('height')
            weight = data.get('weight')
            blood_pressure = data.get('bloodPressure')

            # 데이터 필드 체크
            if not all([username, password, height, weight, blood_pressure]):
                print("Missing field in received data.")  # 디버깅용 메시지
                return JsonResponse({'success': False, 'message': '모든 필드를 입력해주세요.'}, status=400)

            # 사용자 중복 체크
            if User.objects.filter(username=username).exists():
                print("Username already exists.")  # 디버깅용 메시지
                return JsonResponse({'success': False, 'message': '이미 존재하는 사용자입니다.'}, status=400)

            # 사용자 및 프로필 객체 생성 (중복이 없는 경우에만)
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)

                # Profile 객체 생성 및 저장
                Profile.objects.create(
                    user=user,
                    height=float(height) if height else None,
                    weight=float(weight) if weight else None,
                    blood_pressure=float(blood_pressure) if blood_pressure else None
                )

                return JsonResponse({'success': True, 'message': '회원가입 성공', 'redirect_url': '/main/'}, status=201)

        except ValueError as e:
            print("ValueError:", e)  # 디버깅용 출력
            return JsonResponse({'success': False, 'message': f'잘못된 데이터 형식: {str(e)}'}, status=400)

        except IntegrityError as e:
            print("IntegrityError:", e)  # 디버깅용 출력
            return JsonResponse({'success': False, 'message': '사용자 생성 중 오류가 발생했습니다.'}, status=400)

    return JsonResponse({'error': '허용되지 않은 메서드입니다.'}, status=405)