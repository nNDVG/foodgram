from django.contrib import admin

from .models import (Favorites, Follow, Ingredient, Recipe, RecipeList,
                     ShoppingList, Tag)


class IngredientInline(admin.TabularInline):
    '''
    Allows to edit related objects on the same page as
    the parent object. In our projects, we use a linked table
    with the amount of ingredients, so in order to create a
    recipe on one page in the admin panel, we need to pull this
    model into a separate field.
    '''
    extra = 0
    min_num = 1
    model = RecipeList


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    def counter_favorite(self, recipe_id):
        return Favorites.objects.filter(recipe=recipe_id).count()

    counter_favorite.short_description = 'Добавлен в избранное'
    list_display = ('title', 'author', 'counter_favorite')
    list_filter = ('title', 'author', 'tags')
    search_fields = ('title',)
    readonly_fields = ('counter_favorite',)
    empty_value_display = '-пусто-'
    inlines = (IngredientInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('slug', 'name')
    empty_value_display = '-пусто-'


@admin.register(RecipeList)
class RecipeListAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_filter = ('user', 'recipe')
    search_fields = ('user',)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_filter = ('user', 'recipe')
    search_fields = ('user',)
