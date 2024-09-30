from django.urls import path
from django.http import HttpResponseRedirect
from . import views
from .views import WelcomeView

def redirect_to_image_upload(request):
    return HttpResponseRedirect('/image-upload/')

urlpatterns = [
    path('homepage/', WelcomeView.as_view(), name='welcome-api'),  # 기본 경로로 index 뷰를 연결
]