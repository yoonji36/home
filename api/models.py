from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField()
    calorie = models.IntegerField()

    def __str__(self):
        return self.title
