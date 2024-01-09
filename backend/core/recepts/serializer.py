from django.contrib.auth import get_user_model
from rest_framework import serializers

from recepts.models import Ingredients, IngredientsBlacklist, Marinades, Resipes, ResipesIngredients, Sauces, Steps

User = get_user_model()


class SearchIngredientsSerializer(serializers.Serializer):
    query = serializers.CharField(label="Посик ингредиента")


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id','name']

class IngredientsPaginateSerializer(serializers.Serializer):
    count = serializers.CharField(default=None)
    limit = serializers.CharField(default=None)
    total_pages = serializers.CharField(default=None)
    pagination_next = serializers.CharField(default=None)
    list = IngredientsSerializer(many=True)

class IngredientsResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default="ok")
    data = IngredientsPaginateSerializer()

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steps
        fields = ['step', 'text', 'photo']

class ResipesIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientsSerializer()
    class Meta:
        model = ResipesIngredients
        fields = ['amount', 'dimension', 'state', 'ingredient']


class MarinadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marinades
        fields = ['amount', 'dimension', 'state', 'ingredient']
        

class SaucesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sauces
        fields = ['amount', 'dimension', 'state', 'ingredient']
        
      
class ReceptSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    ingredients = ResipesIngredientsSerializer(many=True)
    marinades = MarinadesSerializer(many=True)
    sauces = SaucesSerializer(many=True)
    
    class Meta:
        model = Resipes
        fields = ['id', 'name', 'preview', 'meal_type', 'tags', 'cook_time', 'ingredients', 'marinades', 'sauces', 'steps']


class StatusReceptSerializer(serializers.Serializer):
    status = serializers.CharField(default="ok")
    data = ReceptSerializer()
    
    
class LikesDislikesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
 
 
class RecipeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Resipes
        fields = ['id', 'name', 'preview', 'meal_type', 'tags', 'cook_time']
 
 
class RecipeListSerializer(serializers.Serializer):
    resipes = RecipeSerializer(many=True)
    
    
class RecipeGETSerializer(serializers.Serializer):
    status = serializers.CharField(default="ok")
    data = RecipeListSerializer()
    
    
class IngredientsBlacklistSerializer(serializers.Serializer):
    ingredients_blacklist = serializers.JSONField(default=list)
    

class IngredientsBlacklistGETSerializer(serializers.Serializer):
    status = serializers.CharField(default="ok")
    data = IngredientsBlacklistSerializer()