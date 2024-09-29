from django.urls import path
from . import views
from .views import recipe_list, recipe_detail, get_meal_plan  # OpenAI API 사용

urlpatterns = [
    path('', views.main_page, name='main-page'),  # 기본 메인 페이지 (React에서 관리)
    path('upload/', views.image_upload, name='image_upload'),  # 이미지 업로드 API
    path('api/get-meal-plan/', get_meal_plan, name='get_meal_plan'),  # OpenAI API로 식단 생성
    path('api/recipes/', recipe_list, name='recipe-list'),  # 레시피 목록 API
    path('api/recipes/<int:recipe_id>/', recipe_detail, name='recipe-detail'),  # 레시피 상세 API
]
