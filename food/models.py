from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Метка')
    color = models.CharField(max_length=150, unique=True, verbose_name='Цвет')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    dimension = models.CharField(max_length=150, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='recipe',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='recipe/images', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeList', verbose_name='Ингредиенты', blank=False
    )
    tags = models.ManyToManyField(Tag, verbose_name='Тег', related_name='recipe')
    coocking_time = models.PositiveIntegerField(verbose_name='Время готовки')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class RecipeList(models.Model):
    """Table for link a recipe to an ingredient and setting its quantity"""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipelist', verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество')


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_shopping_list', verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_shopping_list', verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_shop_list')
        ]


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.CheckConstraint(check=~models.Q(user=models.F('author')), name='check_user'),
            models.UniqueConstraint(fields=['user', 'author'], name='unique_follow')
        ]
        ordering = ('author',)


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_favorites')
        ]
