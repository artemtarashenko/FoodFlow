from django.db import models
from django.contrib.auth import get_user_model

from recepts.models import Resipes

User = get_user_model()

class MenuConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="menu_config")
    meal_count = models.IntegerField(blank=True, null=True)
    portions_count = models.IntegerField(blank=True, null=True)
    
    def __str__(self) -> str:
        return super().__str__()
    
    class Meta:
        verbose_name = 'Настройку меню'
        verbose_name_plural = 'Настройки меню'
        

class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_menu")
    start_date = models.DateField(auto_created=True)
    end_date = models.DateField(blank=True, null=True)
    
    def __str__(self) -> str:
        return super().__str__()
    
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        

class RecipeMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_recipe")
    week_day = models.DateField(blank=True, null=True)
    recipe = models.ForeignKey(Resipes, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return super().__str__()
    
    class Meta:
        verbose_name = 'Репт в меню'
        verbose_name_plural = 'Рецепты в меню'