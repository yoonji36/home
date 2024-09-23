from django.urls import path
from django.http import HttpResponseRedirect
from . import views
from .views import index

def redirect_to_image_upload(request):
    return HttpResponseRedirect('/makerecipe/image-upload/')

urlpatterns = [
    path('', index, name='index'),  # 기본 경로로 index 뷰를 연결
    path('', views.main_page, name='main-page'), # 기본 메인 페이지
    path('upload/', views.image_upload, name='image_upload'),
    path('image-upload.html', redirect_to_image_upload),  # 리디렉션
    path('makerecipe/image-upload/', views.image_upload, name="image-upload") # 이미지 업로드 페이지로 이동
]