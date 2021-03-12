def take_ingredients(request):
    """
    We use this function to get ingredients from
    our request when creating / editing recipes.
    """
    ingredients = {}
    for key in request:
        if key.startswith('nameIngredient_'):
            num = key[15:]
            if num.isdecimal():
                ingredients[request[key]] = request[f'valueIngredient_{num}']
    return ingredients
