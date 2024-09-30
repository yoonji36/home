# backend/app/models.py

from django.db import models
# myapp/models.py

from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

<<<<<<< HEAD
=======

>>>>>>> 5dce980497d8ab786192f2bbd4b21caac0025649
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    sodium = models.FloatField()   # 나트륨 함량
    carbs = models.FloatField()    # 탄수화물 함량
    calories = models.FloatField() # 칼로리
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name