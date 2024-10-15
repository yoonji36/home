from django.urls import path
from .views import login_page, signup_page
from main.views import main_page

urlpatterns = [
    path('signup/', signup_page, name='signup-page'),  # 회원가입 페이지 경로
    path('', login_page, name="login-page"), # login_view를 /login URL에 매핑하기
]