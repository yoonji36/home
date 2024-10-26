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
from django.urls import path, include, re_path
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls, name='django-admin'),  # 'admin' 네임스페이스 지정
    path('__debug__/', include('debug_toolbar.urls')),  # Django Debug Toolbar
    path('mdl/', include('mdl.urls')),  # mdl 앱의 URL 패턴 포함
    path('login/', include('login.urls')),  # 메인페이지 URL
    re_path(r'^$', lambda request: redirect('login')),  # /로 접속 시 /login/으로 리디렉션
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])