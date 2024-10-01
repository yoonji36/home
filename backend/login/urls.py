from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # API 경로 설정
    path('login/', views.login_api, name='login-api'),  # 로그인 API 엔드포인트
    path('login/signup/', views.signup_api, name='signup-api'),  # 회원가입 API 엔드포인트

    # 메인 페이지 경로
    path('main/', TemplateView.as_view(template_name='index.html'), name='main-page'),

    # React SPA를 위해 모든 페이지 요청을 index.html로 연결 (가장 마지막에 위치해야 합니다)
    re_path(r'^.*$', TemplateView.as_view(template_name='recipe-app/build/index.html'), name='react-app'),
]