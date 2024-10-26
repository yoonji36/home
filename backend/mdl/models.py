from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    ingredients = models.JSONField()
    instructions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
