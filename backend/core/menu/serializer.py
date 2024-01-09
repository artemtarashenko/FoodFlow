from django.contrib.auth import get_user_model
from rest_framework import serializers

from recepts.serializer import IngredientsSerializer, RecipeSerializer

from .models import Menu, MenuConfig, RecipeMenu, ShopList

User = get_user_model()

class MunuConfigSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuConfig
        fields = ["meal_count", "portions_count"]
        
class RecipeMenuSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()
    class Meta:
        model = RecipeMenu
        fields = ["id", "week_day", "recipe"]


class MunuSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    recipes = RecipeMenuSerializer(many=True)
    
    class Meta:
        model = Menu
        fields = ["id", "user", "start_date", "end_date", "recipes"]

class MenuChildSerializer(serializers.Serializer):
    menu = MunuSerializer()

class MenuDataSerializer(serializers.Serializer):
    status = serializers.CharField(default="ok")
    data = MenuChildSerializer()
    
    
class MenuRecipeIdSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()

        
class ShopIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientsSerializer()
    description = serializers.ListField(
        child=serializers.JSONField(default={"dimension": None, "amount": 0})
        )
    
    class Meta:
        model = ShopList
        fields = ["id", "ingredient", "description", "is_check"]
        

class ShopListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    list = ShopIngredientsSerializer(many=True)
    
    
class ShopListCheckedSerializer(serializers.Serializer):
    cheked = serializers.ListField(child=serializers.IntegerField(default=0))
    not_cheked = serializers.ListField(child=serializers.IntegerField(default=0))
    
class ShopListCheckedResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default="ok")
    data = ShopListCheckedSerializer()