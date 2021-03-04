from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.new_recipe, name='new_recipe'),
    path('<str:username>/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('<str:username>/<int:recipe_id>/delete/', views.del_recipe, name='del_recipe'),
    path('follow/', views.follow_index, name='follow_index'),
    path('favorite/', views.favorite, name='favorite'),
    path('shopping_list', views.shopping_list, name='shopping_list'),
    path('download_shop_list', views.download_shop_list, name='download_shop_list'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('<str:username>/', views.profile, name='profile'),
    path('', views.index, name='index'),
]
