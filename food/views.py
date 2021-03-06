from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from users.models import User
from .forms import RecipeForm
from .models import Follow, Ingredient, Recipe, RecipeList, ShoppingList, Tag
from .utils import take_ingredients


def index(request):
    """View main page"""
    cur_tags = request.GET.getlist('tags')
    if not cur_tags:
        cur_tags = Tag.objects.values_list('slug', flat=True)
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(tags__slug__in=cur_tags).distinct()
    paginator = Paginator(recipes, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'cur_tags': cur_tags,
        'all_tags': all_tags
    }
    return render(request, 'index.html', context)


def profile(request, username):
    """View single user"""
    cur_tags = request.GET.getlist('tags')  # catch current tags
    if not cur_tags:
        cur_tags = Tag.objects.values_list('slug', flat=True)  # if filter empty get all tags
    all_tags = Tag.objects.all()
    username = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=username, tags__slug__in=cur_tags).distinct()
    paginator = Paginator(recipes, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(author=username, user=request.user)
    context = {
        'page': page,
        'paginator': paginator,
        'username': username,
        'following': following,
        'cur_tags': cur_tags,
        'all_tags': all_tags
    }
    return render(request, 'authorRecipe.html', context)


@login_required
def new_recipe(request):
    """New recipe creation function"""
    user = get_object_or_404(User, username=request.user.username)
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            ingredients = take_ingredients(request)
            new_recipe = form.save(commit=False)
            new_recipe.author = user
            new_recipe.save()
            for title in ingredients:
                title_ingredient = get_object_or_404(Ingredient, title=title)
                add_ingredient = RecipeList(
                    recipe=new_recipe,
                    ingredient=title_ingredient,
                    amount=ingredients[title]
                )
                add_ingredient.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def edit_recipe(request, username, recipe_id):
    """Recipe editing function"""
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    if recipe.author != request.user:
        return redirect('recipe_view', username=username, recipe_id=recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if form.is_valid():
        ingredients = take_ingredients(request)
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        RecipeList.objects.filter(recipe_id=recipe.id).delete()
        for title in ingredients:
            title_ingredient = get_object_or_404(Ingredient, title=title)
            add_ingredient = RecipeList(
                recipe=new_recipe,
                ingredient=title_ingredient,
                amount=ingredients[title]
            )
            add_ingredient.save()
        form.save_m2m()
        return redirect('index')
    ingredients = RecipeList.objects.filter(recipe=recipe)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    return render(request, 'formChangeRecipe.html', {'form': form, 'ingredients': ingredients, 'recipe': recipe})


@login_required
def del_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.username == username:
        recipe.delete()
    return redirect('index')


def recipe_view(request, username, recipe_id):
    """View single recipe"""
    username = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    return render(request, 'singlePage.html', {'username': username, 'recipe': recipe})


@login_required
def follow_index(request):
    """View a list of subscriptions"""
    follows = Follow.objects.select_related('user', 'author').filter(user=request.user)
    paginator = Paginator(follows, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page, 'paginator': paginator})


@login_required
def favorite(request):
    """View user favorite list """
    cur_tags = request.GET.getlist('tags')
    if not cur_tags:
        cur_tags = Tag.objects.values_list('slug', flat=True)
    all_tags = Tag.objects.all()
    recipe_list = Recipe.objects.filter(favorites__user=request.user, tags__slug__in=cur_tags).distinct()
    paginator = Paginator(recipe_list, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'cur_tags': cur_tags,
        'all_tags': all_tags
    }
    return render(
        request,
        'favorites.html', context)


@login_required
def shopping_list(request):
    """View shopping list """
    shop_list = ShoppingList.objects.filter(user=request.user).all()
    return render(request, 'shopList.html', {'shop_list': shop_list})


@login_required
def download_shop_list(request):
    """Function for downloading a shopping list in a txt file"""
    recipes = Recipe.objects.filter(recipe_shopping_list__user=request.user)
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension'
    ).annotate(total_amount=Sum('recipelist__amount'))
    print(ingredients)
    file_data = [
        f"{v['ingredients__title'].capitalize()}: {v['ingredients__dimension']} {v['total_amount']}\n"
        for v in ingredients
    ]
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response
