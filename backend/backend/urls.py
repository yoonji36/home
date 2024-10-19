"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls, name='django-admin'),  # 'admin' 네임스페이스 지정
    path('__debug__/', include('debug_toolbar.urls')),  # Django Debug Toolbar
    path('mdl/', include('mdl.urls')),  # mdl 앱의 URL 패턴 포함
    path('', lambda request: redirect('login-page')),  # 기본 경로 -> 로그인 페이지로 리다이렉트
    path('main/', include('main.urls')),  # 메인페이지 URL
    path('login/', include('login.urls')),  # 로그인 및 회원가입
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),  # 로그아웃 처리
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])