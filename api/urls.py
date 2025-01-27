from django.urls import path

from . import views

urlpatterns = [
    path("favorites", views.Favorite.as_view()),
    path("favorites/<int:recipe_id>", views.Favorite.as_view()),
    path("subscriptions", views.Subscribe.as_view()),
    path("subscriptions/<int:author_id>", views.Subscribe.as_view()),
    path("purchases", views.Purchase.as_view()),
    path("purchases/<int:recipe_id>", views.Purchase.as_view()),
    path("ingredients", views.Ingredients.as_view()),
    ]
