from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from . import views

def redirect_to_image_upload(request):
    return HttpResponseRedirect('/makerecipe/image-upload/')

urlpatterns = [
    path('', views.main_page, name='main-page'),
    path('login/', include('login.urls')),  # login 앱의 URL 포함
    path('upload/', views.image_upload, name='image_upload'),
    path('image-upload.html', redirect_to_image_upload),  # 리디렉션
    path('makerecipe/image-upload/', views.image_upload, name="image-upload"), # 이미지 업로드 페이지로 이동
    path('make-recipe/', views.make_recipe, name='make-recipe'),
]