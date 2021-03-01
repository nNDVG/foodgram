from django import template
from food.models import Favorites, Follow, ShoppingList

register = template.Library()


@register.filter(name='subscription_filter')
def subscription_filter(user, author):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='favorite_filter')
def favorite_filter(recipe, user):
    return Favorites.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='bag_filter')
def bag_filter(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('tags')


@register.filter(name='tags_filter')
def tags_filter(request, tag):
    new_request = request.GET.copy()
    if tag.slug in request.GET.getlist('tags'):
        filters = new_request.getlist('tags')
        filters.remove(tag.slug)
        new_request.setlist('tags', filters)
    else:
        new_request.appendlist('tags', tag.slug)
    return new_request.urlencode()

