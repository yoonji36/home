from django.db import models
from django.contrib.auth.models import User

# Profile 모델 생성 (User 모델 확장)
class Myhistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ingredient_list = models.CharField(max_length=300)  # 재료
    chatgpt_response = models.CharField(max_length=2048)  # 래시피
    created_at = models.DateTimeField(auto_now_add=True)
