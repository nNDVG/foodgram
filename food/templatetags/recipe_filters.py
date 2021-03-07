from django import template

from food.models import Favorites, Follow, ShoppingList, Tag

register = template.Library()


"""Filter by subscription"""
@register.filter(name='subscription_filter')
def subscription_filter(user, author):
    return Follow.objects.filter(user=user, author=author).exists()


"""Filter by farovite recipes"""
@register.filter(name='favorite_filter')
def favorite_filter(recipe, user):
    return Favorites.objects.filter(user=user, recipe=recipe).exists()


"""Filter by shop list"""
@register.filter(name='bag_filter')
def bag_filter(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()


"""Filter for create new tag filter"""
@register.filter(name='tags_filter')
def tags_filter(request, tag):
    new_request = request.GET.copy()
    if not new_request.getlist('tags'):
        filters = list(Tag.objects.values_list('slug', flat=True))
        filters.remove(tag.slug)
        new_request.setlist('tags', filters)
        return new_request.urlencode()
    if tag.slug in request.GET.getlist('tags'):
        filters = new_request.getlist('tags')
        filters.remove(tag.slug)
        new_request.setlist('tags', filters)
    else:
        new_request.appendlist('tags', tag.slug)
    return new_request.urlencode()


"""Count recipes in bag"""
@register.filter(name='couter')
def couter(request, user_id):
    count = ShoppingList.objects.filter(user=user_id).count()
    return count
