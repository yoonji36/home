from django.urls import path
from .views import login_page, signup_page

urlpatterns = [
    path('', login_page, name='login-page'),  # 로그인 페이지 경로
    path('signup/', signup_page, name='signup-page'),  # 회원가입 페이지 경로
]
