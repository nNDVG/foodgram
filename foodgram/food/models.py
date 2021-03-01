from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, max_length=20)
    color = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    title = models.CharField(max_length=30)
    dimension = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='recipe')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipe/')
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeList')
    tags = models.ManyToManyField(Tag)
    coocking_time = models.IntegerField()

    def __str__(self):
        return self.title


class RecipeList(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipelist')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredients')
    amount = models.IntegerField(default=1)


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_shopping_list'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_shopping_list'
    )


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')

