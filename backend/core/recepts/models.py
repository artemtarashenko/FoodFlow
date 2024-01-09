import uuid
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model

from .fields import WEBPField

User = get_user_model()

def image_folder(instance, filename):
    return '{}.webp'.format(uuid.uuid4().hex)


class Resipes(models.Model):
    types = [
        ("1", "breakfast"),
        ("2", "lunch"),
        ("3", "dinner")
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    preview = WEBPField(blank=True, null=True, upload_to=image_folder)
    meal_type = models.CharField(choices=types, max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True)
    cook_time = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def img_preview(self):
        if self.preview:
            return mark_safe('<img src="{url}" width="60px"/>'.format(url=self.preview.url))
        return mark_safe('<img src="{url}" width="60px"/>'.format(url="/media/blank.png"))

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredients(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Dimensions(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    number = models.IntegerField(verbose_name='Номер')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['number']
        verbose_name = 'Едицу измерения'
        verbose_name_plural = 'Едицы измерения'
        
    
class ResipesIngredients(models.Model):
    resipe = models.ForeignKey(Resipes, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='ingredients')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, verbose_name='Название')
    amount = models.FloatField(default=0, verbose_name='кол-во')
    dimension = models.ForeignKey(Dimensions, on_delete=models.CASCADE, blank=True, null=True, verbose_name='единица')
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name='состояние')
    
    def __str__(self) -> str:
        return self.resipe.name
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        

class Marinades(models.Model):
    resipe = models.ForeignKey(Resipes, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='marinades')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, verbose_name='Название')
    amount = models.FloatField(default=0, verbose_name='кол-во')
    dimension = models.ForeignKey(Dimensions, on_delete=models.CASCADE, blank=True, null=True, verbose_name='единица')
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name='состояние')

    def __str__(self) -> str:
        return self.resipe.name
    
    class Meta:
        verbose_name = 'Маринад'
        verbose_name_plural = 'Маринады'
        

class Sauces(models.Model):
    resipe = models.ForeignKey(Resipes, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='sauces')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, verbose_name='Название')
    amount = models.FloatField(default=0, verbose_name='кол-во')
    dimension = models.ForeignKey(Dimensions, on_delete=models.CASCADE, blank=True, null=True, verbose_name='единица')
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name='состояние')

    def __str__(self) -> str:
        return self.resipe.name

class Steps(models.Model):
    resipe = models.ForeignKey(Resipes, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='steps')
    step = models.IntegerField(blank=True, null=True, verbose_name='Шаг')
    text = models.TextField(verbose_name='Описание')
    photo = WEBPField(verbose_name='Фото', upload_to=image_folder, blank=True, null=True)
    
    def img_preview(self):
        if self.photo:
            return mark_safe('<img src="{url}" width="60px"/>'.format(url=self.photo.url))
        return mark_safe('<img src = "{url}" width="60px"/>'.format(url="/media/blank.png"))
    
    def __str__(self) -> str:
        return self.resipe.name
        
class ResipesLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='likes')
    recipe = models.ForeignKey(Resipes, on_delete=models.CASCADE, verbose_name='Рецепт')
    

class ResipesDislikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='dislikes')
    recipe = models.ForeignKey(Resipes, on_delete=models.CASCADE, verbose_name='Рецепт')
    

class IngredientsBlacklist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='ingredients_blacklist')
    ingredients_blacklist = models.JSONField(blank=True, null=True)