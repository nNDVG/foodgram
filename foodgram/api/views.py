from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from food.models import Favorites, Follow, Ingredient, Recipe, ShoppingList
from rest_framework.utils import json
from users.models import User


class Favorite(LoginRequiredMixin, View):

    def post(self, request):
        body = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(body['id']))
        user = request.user
        Favorites.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        Favorites.objects.filter(user=user, recipe=recipe).delete()
        return JsonResponse({'success': True})


class Subscribe(LoginRequiredMixin, View):

    def post(self, request):
        request_body = json.loads(request.body)
        author = get_object_or_404(User, id=int(request_body['id']))
        user = request.user
        Follow.objects.get_or_create(user=user, author=author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        user = request.user
        Follow.objects.filter(user=user, author=author).delete()
        return JsonResponse({'success': True})


class Purchase(LoginRequiredMixin, View):

    def post(self, request):
        body = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(body['id']))
        user = request.user
        ShoppingList.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        ShoppingList.objects.filter(user=user, recipe=recipe).delete()
        return JsonResponse({'success': True})


class Ingredients(LoginRequiredMixin, View):

    def get(self, request):
        query = request.GET.get('query', None)
        ingredients = Ingredient.objects.filter(
            title__icontains=query).values('title', 'dimension').order_by('title')
        return JsonResponse(list(ingredients), safe=False)

