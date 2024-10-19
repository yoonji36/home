# backend/login/models.py

from django.db import models
from django.contrib.auth.models import User

# Profile 모델 생성 (User 모델 확장)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_sugar_target = models.IntegerField(default=100)  # 기본값 설정
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    bmi = models.FloatField(null=True, blank=True)

# **models.py**에 기본값을 정의하고, 다시 마이그레이션을 수행하는 방법
    def __str__(self):
        return f'{self.user.username} - Profile'
