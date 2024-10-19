from django.urls import path, re_path
from django.views.static import serve
from . import views
import os

# 정확한 경로로 수정 (frontend 폴더의 절대경로를 지정)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))

urlpatterns = [
    # image_path를 인자로 받음
    path('upload/', views.image_upload, name='image_upload'),  # 이미지 업로드
    path('process_image/<str:image_path>/', views.process_image, name='process_image'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('delete_ingredient/', views.delete_ingredient, name='delete_ingredient'),
    path('api/recipe/', views.generate_recipe, name='generate_recipe'),
    re_path(r'^recipes/$', serve, {
        'document_root': os.path.join(os.path.dirname(__file__), '../../frontend'),
        'path': 'recipes.html'
    }, name='recipes'),
]