from django.urls import path
from . import views
from .views import WelcomeView

urlpatterns = [
    # API 경로
    path('login/', views.login_api, name='login-api'),  # 로그인 API 엔드포인트
    path('signup/', views.signup_api, name='signup-api'),  # 회원가입 API 엔드포인트

    # 다른 기존 URL 패턴들도 여기에 추가
    path('homepage/', WelcomeView.as_view(), name='main-page'),  # 메인 페이지로 리다이렉트 시 사용할 경로 예시
]
