from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, ModelForm

from .models import Recipe
from .utils import take_ingredients


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'tags', 'coocking_time', 'author']
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }

    def clean(self):
        ingredients = take_ingredients(self.data)
        if not ingredients:
            raise ValidationError('Необходимо добавить ингредиент')
