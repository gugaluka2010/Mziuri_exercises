
from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path('recipes/', views.recipe_list, name='list'),
    path('recipes/stats/', views.stats, name='stats'),
    path('recipes/random/', views.random_recipe, name='random'),
    path('recipes/search/', views.search, name='search'),
    path('recipes/category/<str:name>/', views.category_detail, name='category'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='detail'),
    path('recipes/<slug:slug>/', views.recipe_by_slug, name='slug'),
]
