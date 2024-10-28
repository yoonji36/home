from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from mdl.models import Recipe
import requests



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
    news_items = fetch_news_items()
    context = {
        'user_email': user.id,
        'user_bmi': user.weight / ((user.height / 100) ** 2) if user.height and user.weight else None,
        'target_blood_sugar': user.blood_sugar_target,
        'news_items': news_items,
    }
    return render(request, 'home.html', context)

def fetch_news_items():
    client_id = "AMvmbd0mAWudLgFjBOzz"
    client_secret = "5KFOSHoXWw"
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "query": "당뇨",
        "display": 6,
        "sort": "date",
    }

    response = requests.get(url, headers=headers, params=params)
    news_items = []

    if response.status_code == 200:
        data = response.json()
        news_items = data.get("items", [])

    return news_items

@csrf_exempt
def fetch_news(request):
    if request.method == "GET":
        news_items = fetch_news_items()
        return JsonResponse(news_items, safe=False)
    return JsonResponse({"error": "Invalid request"}, status=400)

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
    recipes = Recipe.objects.filter(user=request.user).values('id', 'title')
    return JsonResponse({'recipes': list(recipes)}, status=200)

@login_required
def recipe_detail_view(request, recipe_id):
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
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

@login_required
def myprofile_view(request):
    user = request.user
    context = {
        'user_email': user.id,
        'height': user.height,
        'weight': user.weight,
        'blood_sugar': user.blood_sugar_target,
    }
    return render(request, 'myprofile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        data = request.POST
        user = request.user
        
        user.height = data.get('height')
        user.weight = data.get('weight')
        user.blood_sugar_target = data.get('blood_sugar_target')
        user.save()
        messages.success(request, '프로필이 업데이트되었습니다.')
        return redirect('myprofile')  # 업데이트 후 프로필 페이지로 리다이렉트

    return redirect('myprofile')  # GET 요청 시 프로필 페이지로 리다이렉트
