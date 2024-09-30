from django.contrib import admin  # 이 줄이 필요합니다.
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 관리자 경로
    path('', include('main.urls')),  # main 앱의 URL 패턴 포함
    path('login/', include('login.urls')),  # 로그인 및 회원가입
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그아웃
]
