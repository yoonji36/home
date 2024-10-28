from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests, json, mdl.models
from .models import User
import logging

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('id')

            # 중복된 사용자 확인
            if User.objects.filter(id=user_id).exists():
                form.add_error('id', '이미 존재하는 아이디입니다.')
                return render(request, 'signup.html', {'form': form})

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('login')

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('id', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=user_id, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '일치하는 사용자가 없습니다.')

    return render(request, 'login.html')

@login_required
def home_view(request):
    user = request.user
    context = {
        'user_email': user.id,  # 사용자 아이디 (이메일로 사용할 경우)
        'user_bmi': user.weight / ((user.height / 100) ** 2) if user.height and user.weight else None,
        'target_blood_sugar': user.blood_sugar_target
    }
    return render(request, 'home.html', context)

@login_required
def home_view(request):
    # 네이버 뉴스 API 설정
    client_id = "AMvmbd0mAWudLgFjBOzz"  # 네이버 클라이언트 ID
    client_secret = "5KFOSHoXWw"  # 네이버 클라이언트 시크릿
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "query": "당뇨",
        "display": 7,  # 뉴스 5개만 가져오기
        "sort": "date",  # 최신 순으로 정렬
    }

    response = requests.get(url, headers=headers, params=params)
    news_items = []

    if response.status_code == 200:
        data = response.json()
        news_items = data.get("items", [])

    context = {
        'user_email': request.user.id,
        'user_bmi': request.user.weight / ((request.user.height / 100) ** 2) if request.user.height and request.user.weight else None,
        'target_blood_sugar': request.user.blood_sugar_target,
        'news_items': news_items,  # 뉴스 데이터 전달
    }

    return render(request, 'home.html', context)

@csrf_exempt
def fetch_news(request):
    if request.method == "GET":
        client_id = "AMvmbd0mAWudLgFjBOzz"  # 네이버 클라이언트 ID
        client_secret = "5KFOSHoXWw"  # 네이버 클라이언트 시크릿
        query = "당뇨"
        display = 7
        start = int(request.GET.get("start", 1))  # 요청에서 시작 위치를 가져옴

        url = "https://openapi.naver.com/v1/search/news.json"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        }
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": "date",
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            news_items = data.get("items", [])
            return JsonResponse(news_items, safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch news"}, status=400)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def myrecord_view(request):
    user = request.user
    context = {
        'user_email': user.id,
        'user_height': user.height,
        'user_weight': user.weight,
        'user_blood_sugar_target': user.blood_sugar_target,
    }
    return render(request, 'myrecord.html', context)

@login_required
def get_user_recipes(request):
    Recipe = mdl.models.Recipe
    recipes = Recipe.objects.filter(user=request.user).values('id', 'title')
    return JsonResponse({'recipes': list(recipes)}, status=200)

@login_required
def recipe_detail_view(request, recipe_id):
    Recipe = mdl.models.Recipe
    try:
        recipe = Recipe.objects.get(id=recipe_id, user=request.user)
        data = {
            'title': recipe.title,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
        }
        return JsonResponse(data, status=200)
    except Recipe.DoesNotExist:
        return JsonResponse({'error': '레시피를 찾을 수 없습니다.'}, status=404)

@login_required
def recipe_detail(request, recipe_id):
    Recipe = mdl.models.Recipe
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

@login_required
def myprofile_view(request):
    user = request.user
    context = {
        'user_email': user.id,
        'height': user.height,
        'weight': user.weight,
        'blood_sugar_target': user.blood_sugar_target,
    }
    return render(request, 'myprofile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:    # 데이터를 처리하는 로직 (예: 데이터베이스 업데이트)
            data = request.POST
            user = request.user
            
            user.height = data.get('height')
            user.weight = data.get('weight')
            user.blood_sugar_target = data.get('blood_sugar_target')
            user.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=500)
    redirect('{% url myprofile %} ')  # GET 요청 시 프로필 페이지로 리다이렉트
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=400)
