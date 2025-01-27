from django import template

from food.models import Favorites, Follow, ShoppingList, Tag

register = template.Library()


@register.filter(name='subscription_filter')
def subscription_filter(user, author):
    """Filter by subscription"""
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='favorite_filter')
def favorite_filter(recipe, user):
    """Filter by farovite recipes"""
    return Favorites.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='bag_filter')
def bag_filter(recipe, user):
    """Filter by shop list"""
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='tags_filter')
def tags_filter(request, tag):
    """Filter for create new tag filter"""
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


@register.filter(name='couter')
def couter(request, user_id):
    """Count recipes in bag"""
    count = ShoppingList.objects.filter(user=user_id).count()
    return count


@register.filter(name='word_end_filter')
def word_end_filter(word, count):
    """Word end filter"""
    count = count - 3
    remainder_ten = count % 10
    remainder_hundred = count % 100
    if remainder_ten == 0:
        word += 'ов'
    elif remainder_ten == 1 and remainder_hundred != 11:
        word += ''
    elif remainder_ten < 5 and remainder_hundred not in [11, 12, 13, 14]:
        word += 'а'
    else:
        word += 'ов'
    return word