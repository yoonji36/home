import json
from django.db import models
from django.conf import settings

class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='recipes')  # 사용자를 ForeignKey로 연결
    title = models.CharField(max_length=200)  # 레시피 제목
    ingredients = models.TextField()  # 재료
    instructions = models.TextField()  # 조리법
    created_at = models.DateTimeField(auto_now_add=True)  # 레시피 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 레시피 수정 시간

    def __str__(self):
        return self.title  # 레시피 제목으로 표현
    
    def save(self, *args, **kwargs):
        # Python 객체를 JSON 문자열로 변환
        self.ingredients = json.dumps(self.ingredients)
        self.instructions = json.dumps(self.instructions)
        super().save(*args, **kwargs)
