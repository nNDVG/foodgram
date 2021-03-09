from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.utils import json

from food.models import Favorites, Follow, Ingredient, Recipe, ShoppingList
from users.models import User


class Favorite(LoginRequiredMixin, View):

    def post(self, request):
        """Add to favorites"""
        body = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(body['id']))
        user = request.user
        Favorites.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        """Delete from favorites"""
        Favorites.objects.filter(user=request.user, recipe__id=recipe_id).delete()
        return JsonResponse({'success': True})


class Subscribe(LoginRequiredMixin, View):

    def post(self, request):
        """Subscribe for author"""
        request_body = json.loads(request.body)
        author = get_object_or_404(User, id=int(request_body['id']))
        user = request.user
        Follow.objects.get_or_create(user=user, author=author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        """Unsubscribe from the author"""
        Follow.objects.filter(user=request.user, author=author_id).delete()
        return JsonResponse({'success': True})


class Purchase(LoginRequiredMixin, View):

    def post(self, request):
        """Add to bag"""
        body = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(body['id']))
        user = request.user
        ShoppingList.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        """Delete from bag"""
        ShoppingList.objects.filter(user=request.user, recipe__id=recipe_id).delete()
        return JsonResponse({'success': True})


class Ingredients(LoginRequiredMixin, View):

    def get(self, request):
        """
        This API is needed to get ingredients by matching
        in the existing database when filling in the ingredient
        name on the recipe creation / editing page.
        """
        query = request.GET.get('query', None)
        ingredients = Ingredient.objects.filter(
            title__istartswith=query).values('title', 'dimension').order_by('title')
        return JsonResponse(list(ingredients), safe=False)
