# backend/app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/recognize-ingredients/', views.recognize_ingredients, name='recognize_ingredients'),
    path('api/generate-recipes/', views.generate_recipes, name='generate_recipes'),
]