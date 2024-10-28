from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # 기본 로그인 페이지
    path('signup/', views.signup, name='signup_page'),  # 회원가입 페이지
    path('main/', views.home_view, name='home'),  # 홈 페이지
    # 중복된 'myapp/' 경로는 제거합니다.
    path('logout/', views.logout_view, name='logout'),
    path('fetch-news/', views.fetch_news, name='fetch_news'),  # 뉴스 가져오는 API URL 추가
    path('myrecord/', views.myrecord_view, name='myrecord'),
    path('get_user_recipes/', views.get_user_recipes, name='get_user_recipes'),
    path('recipe/<int:recipe_id>/', views.recipe_detail_view, name='recipe_detail'),  # 상세 보기 엔드포인트
    path('myprofile/', views.myprofile_view, name='myprofile'),
    path('update-profile/', views.update_profile, name='update_profile'),
]
