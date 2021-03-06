from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.utils import json

from food.models import Favorites, Follow, Ingredient, Recipe, ShoppingList
from users.models import User


class Favorite(LoginRequiredMixin, View):
    """Add to favorites """
    def post(self, request):
        body = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(body['id']))
        user = request.user
        Favorites.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse({'success': True})
    """Delete from favorites """
    def delete(self, request, recipe_id):
        Favorites.objects.filter(user=request.user, recipe__id=recipe_id).delete()
        return JsonResponse({'success': True})


class Subscribe(LoginRequiredMixin, View):
    """Subscribe for author"""
    def post(self, request):
        request_body = json.loads(request.body)
        author = get_object_or_404(User, id=int(request_body['id']))
        user = request.user
        Follow.objects.get_or_create(user=user, author=author)
        return JsonResponse({'success': True})
    """Unsubscribe from the author"""
    def delete(self, request, author_id):
        Follow.objects.filter(user=request.user, author=author_id).delete()
        return JsonResponse({'success': True})


class Purchase(LoginRequiredMixin, View):
    """Add to bag"""
    def post(self, request):
        body = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(body['id']))
        user = request.user
        ShoppingList.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse({'success': True})
    """Delete from bag"""
    def delete(self, request, recipe_id):
        ShoppingList.objects.filter(user=request.user, recipe__id=recipe_id).delete()
        return JsonResponse({'success': True})


class Ingredients(LoginRequiredMixin, View):
    """
    This API is needed to get ingredients by matching
    in the existing database when filling in the ingredient
    name on the recipe creation / editing page.
    """
    def get(self, request):
        query = request.GET.get('query', None)
        ingredients = Ingredient.objects.filter(
            title__istartswith=query).values('title', 'dimension').order_by('title')
        return JsonResponse(list(ingredients), safe=False)
