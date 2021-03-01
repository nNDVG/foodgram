from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from users.models import User

from .utils import take_ingredients
from .forms import RecipeForm
from .models import Ingredient, Follow, Recipe, RecipeList, ShoppingList, Tag


def index(request):
    cur_tags = request.GET.getlist('tags')
    if not cur_tags:
        cur_tags = Tag.objects.values_list('slug', flat=True)
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(tags__slug__in=cur_tags).distinct()
    paginator = Paginator(recipes, 6)
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
    cur_tags = request.GET.getlist('tags')
    if not cur_tags:
        cur_tags = Tag.objects.values_list('slug', flat=True)
    all_tags = Tag.objects.all()
    username = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=username, tags__slug__in=cur_tags).order_by('-pub_date').all()
    paginator = Paginator(recipes, 6)
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
                add_ingredient = RecipeList(recipe=new_recipe, ingredient=title_ingredient, amount=ingredients[title])
                add_ingredient.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def edit_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    if recipe.author != request.user:
        return redirect('recipe_view', username=username, recipe_id=recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    print(form)
    if form.is_valid():
        ingredients = take_ingredients(request)
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        RecipeList.objects.filter(recipe_id=recipe.id).delete()
        for title in ingredients:
            title_ingredient = get_object_or_404(Ingredient, title=title)
            add_ingredient = RecipeList(recipe=new_recipe, ingredient=title_ingredient, amount=ingredients[title])
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
    username = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    return render(request, 'singlePage.html', {'username': username, 'recipe': recipe})


@login_required
def follow_index(request):
    follows = Follow.objects.select_related('user', 'author').filter(user=request.user)
    paginator = Paginator(follows, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page, 'paginator': paginator})


@login_required
def favorite(request):
    cur_tags = request.GET.getlist('tags')
    if not cur_tags:
        cur_tags = Tag.objects.values_list('slug', flat=True)
    all_tags = Tag.objects.all()
    recipe_list = Recipe.objects.filter(favorites__user=request.user, tags__slug__in=cur_tags).order_by('-pub_date').all()
    paginator = Paginator(recipe_list, 6)
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
    shop_list = ShoppingList.objects.filter(user=request.user).all()
    return render(request, 'shopList.html', {'shop_list': shop_list})


@login_required
def download_shop_list(request):
    recipes = Recipe.objects.filter(recipe_shopping_list__user=request.user)
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension'
    ).annotate(total_amount=Sum('recipelist__amount'))
    file_data = ''
    for item in ingredients:
        line = ' '.join(str(value) for value in item.values())
        file_data += line + '\n'
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response
