from django.urls import path
from .views import main_page, my_records, create_recipe

urlpatterns = [
    path('', main_page, name='main-page'),
    path('my-records/', my_records, name='my-records'),
    path('create-recipe/', create_recipe, name='create-recipe'),
]
