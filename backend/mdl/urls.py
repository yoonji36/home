from django.urls import path
from . import views
from .views import recipe_list, RecipeDetailView, ImageUploadView

urlpatterns = [
    # image_path를 인자로 받음
    path('image_upload/', ImageUploadView.as_view(), name = 'image_upload'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('delete_ingredient/', views.delete_ingredient, name='delete_ingredient'),
    path('recipe_list/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', RecipeDetailView.as_view(), name='recipe-detail'),
]