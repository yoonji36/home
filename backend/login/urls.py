from django.urls import path
from .views import login_page, signup_page
from main.views import main_page
from . import views
import include

urlpatterns = [
    path('', views.login_page, name='login-page'),  # 로그인 페이지
    path('signup/', views.signup_page, name='signup_page'),  # 회원가입 페이지
]