from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Profile
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.middleware.csrf import get_token
import json
from django.db import transaction
from decimal import Decimal, InvalidOperation
from django.views.decorators.http import require_http_methods
import logging
logger = logging.getLogger(__name__)

# 로그인 페이지 렌더링 시 CSRF 쿠키 설정
@ensure_csrf_cookie
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token}, status=200)

# 로그인 API
# 로그인 API
@csrf_protect
def login_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': '로그인 성공',
                    'redirect_url': '/HomePage',
                    'user_id': user.id,
                    'username': user.username
                })
            else:
                return JsonResponse({'success': False, 'message': '로그인 실패'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '잘못된 요청 형식입니다.'}, status=400)

    return JsonResponse({'error': '허용되지 않은 메서드입니다.'}, status=405)

@csrf_protect
@require_http_methods(["POST"])
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'success': True,
            'message': '로그인 성공',
            'redirect_url': '/HomePage',
            'user_id': user.id,
            'username': user.username
        })
    else:
        return JsonResponse({'success': False, 'message': '로그인 실패'}, status=400)

# 회원가입 API
def signup_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            height = data.get('height')
            weight = data.get('weight')
            blood_pressure = data.get('bloodPressure')

            logger.info(f"Received data: {data}")

            if not all([username, password, height, weight, blood_pressure]):
                return JsonResponse({'success': False, 'message': '모든 필드를 입력해주세요.'}, status=400)

            try:
                height = float(height)
                weight = float(weight)
                blood_pressure = str(blood_pressure)
            except ValueError:
                return JsonResponse({'success': False, 'message': '키와 몸무게는 숫자여야 합니다.'}, status=400)

            with transaction.atomic():
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'success': False, 'message': '이미 존재하는 사용자입니다.'}, status=400)

                user = User.objects.create_user(username=username, password=password)

                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'height': height,
                        'weight': weight,
                        'blood_pressure': blood_pressure
                    }
                )

                if not created:
                    profile.height = height
                    profile.weight = weight
                    profile.blood_pressure = blood_pressure
                    profile.save()

                logger.info(f"User created: {user}, Profile created: {created}")

            return JsonResponse({'success': True, 'message': '회원가입 성공', 'redirect_url': '/main/'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '잘못된 JSON 형식입니다.'}, status=400)

        except Exception as e:
            logger.exception(f"Unexpected error during signup: {e}")
            return JsonResponse({'success': False, 'message': f'서버 오류: {str(e)}'}, status=500)

    return JsonResponse({'error': '허용되지 않은 메서드입니다.'}, status=405)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})