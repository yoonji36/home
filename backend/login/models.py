# backend/login/models.py

from django.db import models
from django.contrib.auth.models import User

# Profile 모델 생성 (User 모델 확장)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 키
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 몸무게
    blood_pressure = models.CharField(max_length=50, null=True, blank=True)  # 혈압

    def __str__(self):
        return self.user.username
