from django.urls import path, include

from main.views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('category/<str:slug>/', category_detail, name='category'),
    path('recipe/<int:pk>/', recipe_detail, name='detail'),
    path('add-recipe/', add_recipe, name='add-recipe'),
    path('update-recipe/<int:pk>/', update_recipe, name='update-recipe'),
    path('delete-recipe/<int:pk>/', delete_recipe, name='delete-recipe'),
]