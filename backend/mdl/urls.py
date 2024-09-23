from django.urls import path
from . import views
from .views import recipe_list, recipe_detail

urlpatterns = [
    # image_path를 인자로 받음
    path('process_image/<str:image_path>/', views.process_image, name='process_image'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('delete_ingredient/', views.delete_ingredient, name='delete_ingredient'),
    path('recipe_list/', views.recipe_list, name='recipe_list'),
    path('recipes/', recipe_list, name='recipe-list'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe-detail'),
]