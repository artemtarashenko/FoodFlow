from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth import get_user_model

from recepts.serializer import ResipesIngredientsSerializer

from recepts.models import Ingredients, Resipes, ResipesDislikes

User = get_user_model()

class MenuConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="menu_config")
    meal_count = models.IntegerField(blank=True, null=True)
    portions_count = models.IntegerField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.user.email
    
    class Meta:
        verbose_name = 'Настройку меню'
        verbose_name_plural = 'Настройки меню'
        

class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_menu")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    is_history = models.BooleanField(default=False)
    
    def recipes(self):
        return self.menu_recipe
    
    def __str__(self) -> str:
        return self.user.name
    
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        
    def generate_end_date(self):
        """
        Генерирует дату на концец недели
        """
        end_date = self.start_date
        for n in range(7):
            if end_date.weekday() == 6:
                break
            end_date += timedelta(days=1)
        
        self.end_date = end_date
        self.save()
        
        return self
    
    def generate_menu(self, likes, dislike, black_list):
        """
        Генерирует меню на неделю
        """
        curent_date = datetime.now().date() # текущая дата
        new_generate_date = self.end_date + timedelta(days=1) # +1 день на конец даты в меню 
        if curent_date >= new_generate_date: # если текущая дата больше или равна следующего дня конечной даты в меню то меню поподает в историю
            self.is_history = True
            self.save()
            self = Menu(user=self.user) # Создаем новое меню с текущей датой
            self.generate_end_date()
        
        menu_config = self.user.menu_config
        meal_count = menu_config.meal_count
        week_day = self.start_date
        range_date = (self.end_date - self.start_date).days + 1
        for n in range(range_date if range_date > 0 else 1):
            resipes = Resipes.objects.exclude(id__in=dislike, ingredients__id__in=black_list).order_by('?')[:meal_count]
            for resipe in resipes:
                recipe_menu = RecipeMenu.objects.filter(menu=self, date=week_day)
                if recipe_menu.count() < meal_count:
                    recipe_menu = RecipeMenu(menu=self, date=week_day, recipe=resipe)
                    recipe_menu.save()
            week_day += timedelta(days=1)
        
        return self

    
    def shop_ingredients_update_or_create(self, objects):
        """ 
        Обновляет или создает список покупок на неделю для меню
        """
        list_id = []
        for obj in objects:
            ingredient = obj["ingredient"]
            description = obj["description"]
            shop_ingredient = ShopList.objects.filter(menu=self, ingredient=ingredient).first()
            if shop_ingredient:
                if description != shop_ingredient.description: 
                    shop_ingredient.is_check = False    
                shop_ingredient.description = description
                shop_ingredient.save()
            else:
                shop_ingredient = ShopList(menu=self, ingredient=ingredient, description=description)
                shop_ingredient.save()
           
            list_id.append(ingredient.id)
        
        delete_not_list = ShopList.objects.exclude(ingredient_id__in=list_id).delete()
        
        return self
        
    def shop_list_create_or_update(self):
        """
        формирует список покупок на неделю с умножением на количество порций
        """
        menu_config = self.user.menu_config
        portions_count = menu_config.portions_count
        menu_recipe = self.menu_recipe.all()
        
        combined_query = [] 
        for obj in menu_recipe: combined_query.extend(
            obj.recipe.ingredients.all().union(
                obj.recipe.marinades.all(), obj.recipe.sauces.all()))
        
        shop_ingredients = []
        for obj in combined_query:
            shop_ingredients.append({
                "ingredient": obj.ingredient,
                "description": [{"dimension": f"{obj.dimension}", "amount": obj.amount}]                 
                }) 

        result = []
        temp_dict = {}
        for item in shop_ingredients:
            ingredient = item["ingredient"]
            description_dimension = item["description"][0]["dimension"]
            description_amount = item["description"][0]["amount"] * portions_count
            
            if ingredient not in temp_dict:
                temp_dict[ingredient] = {"ingredient": ingredient, "description": {}}
            
            existing_description = temp_dict[ingredient]["description"]
            
            if description_dimension not in existing_description:
                existing_description[description_dimension] = description_amount
            else:
                existing_description[description_dimension] += description_amount
            
        result = [{
            "ingredient": v["ingredient"], 
            "description": [{"dimension": k, "amount": v["description"][k]} for k in v["description"]]
            } for v in temp_dict.values()]
        
        return self.shop_ingredients_update_or_create(result)
    

class RecipeMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_recipe")
    date = models.DateField(blank=True, null=True)
    recipe = models.ForeignKey(Resipes, on_delete=models.CASCADE)
    
    weekdays = {1: "mon", 2: "tue", 3: "wed", 4: "thu", 5: "fri", 6: "sat", 7: "sun"}
    
    @property
    def week_day(self):
        day = self.date.isoweekday()
        return self.weekdays.get(day)
    
    def __str__(self) -> str:
        return f"{self.menu}"
    
    class Meta:
        ordering = ["date"]
        verbose_name = 'Репт в меню'
        verbose_name_plural = 'Рецепты в меню'
        

class ShopList(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="shop_ingredients")
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, verbose_name='Название')
    description = models.JSONField(blank=True, null=True)
    is_check = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.ingredient}"
    
    class Meta:
        ordering = ["id"]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'