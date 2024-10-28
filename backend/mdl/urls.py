from django.urls import path, re_path
from django.views.static import serve
from . import views
from . views import get_ingredients_from_session, get_recipe_from_session
import os

# 정확한 경로로 수정 (frontend 폴더의 절대경로를 지정)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))

urlpatterns = [
    # 이미지 업로드 관련 URL
    path('upload_page/', views.upload_view, name='upload_page'),
    path('upload/', views.image_upload, name='image_upload'),  # 이미지 업로드
    path('process_image/<str:image_path>/', views.process_image, name='process_image'),
    
    # 재료 추가 및 삭제 관련 URL
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('delete_ingredient/', views.delete_ingredient, name='delete_ingredient'),
    
    # 재료 및 칼로리 저장/조회 API
    path('api/save_ingredients/', views.save_ingredients_and_calorie, name='save_ingredients'),
    path('api/get_ingredients/', get_ingredients_from_session, name='get_ingredients'),
    path('api/get_recipe/', get_recipe_from_session, name='get_recipe'),
    
    # 레시피 생성 API
    path('api/recipe/', views.generate_recipe, name='generate_recipe'),

    # 레시피 저장 
    path('api/save_recipe/', views.save_recipe, name='save_recipe'),  # 누락된 경로 추가

    # 레시피 페이지 URL 정의
    path('recipes/', views.recipes_page, name='recipes'),  # recipes 페이지 URL 정의
]