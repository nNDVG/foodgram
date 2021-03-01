from django.contrib import admin


from .models import Follow, Favorites, Ingredient, Recipe, RecipeList, ShoppingList, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'id')
    list_filter = ('title', 'author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_filter = ['title']
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    empty_value_display = '-пусто-'


@admin.register(RecipeList)
class RecipeListAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'amount']
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_filter = ['user', 'recipe']


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_filter = ['user', 'recipe']

