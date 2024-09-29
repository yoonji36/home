from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)  # 레시피 이름
    image_url = models.URLField()            # 레시피 이미지 URL
    ingredients = models.TextField()         # 재료 리스트 (텍스트)
    cooking_steps = models.TextField()       # 조리 과정 (텍스트)
    cooking_image_url = models.URLField()    # 조리 과정 이미지 URL
    nutrition_info = models.TextField()      # 영양 정보 (옵션)

    def __str__(self):
        return self.name
