from django.forms import CheckboxSelectMultiple, ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'tags', 'coocking_time', 'author']
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }

