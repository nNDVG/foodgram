def take_ingredients(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if "nameIngredient" in key:
            number_ingredient = key.split("_")
            ingredients[ingredient_name] = int(request.POST[f"valueIngredient_{number_ingredient[1]}"])
    return ingredients
