def take_ingredients(request):
    """
    We use this function to get ingredients from
    our POST request when creating / editing recipes.
    """
    ingredients = {}
    for key in request.POST:
        if key.startswith(f'nameIngredient_'):
            num = key[15:]
            if num.isdecimal():
                ingredients[request.POST[key]] = request.POST[f'valueIngredient_{num}']
    return ingredients
