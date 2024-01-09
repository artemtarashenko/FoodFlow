from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from django.db.models import Sum, Value, Count, F
from django.db.models.functions import Concat, Upper

from recepts.models import IngredientsBlacklist, Resipes, ResipesDislikes, ResipesLikes

from menu.serializer import MenuDataSerializer, MenuRecipeIdSerializer, MunuSerializer, ShopIngredientsSerializer, ShopListCheckedResponseSerializer, ShopListCheckedSerializer, ShopListSerializer
from menu.models import Menu



class MenuViewSet(viewsets.GenericViewSet):
    """Возвращает актуальное меню на неделю и список покупок"""
    queryset = Menu.objects.all()
    serializer_class = MenuDataSerializer
    
    def get_queryset(self):
        return Menu.objects.filter(user=self.request.user)
    
    
    def list(self, request):
        menu = Menu.objects.filter(user=request.user, is_history=False).first()
        likes = ResipesLikes.objects.filter(user=request.user).values_list("recipe__id", flat=True)
        dislike = ResipesDislikes.objects.filter(user=request.user).values_list("recipe__id", flat=True)
        black_list = IngredientsBlacklist.objects.filter(user=request.user).values_list("ingredients_blacklist", flat=True)[0]
        if not menu:
            menu = Menu.objects.create(user=request.user)
            menu.generate_end_date()
        
        menu.generate_menu(likes, dislike, black_list)
        serializer = self.get_serializer({"data": {"menu":menu}})
        return Response(serializer.data)
    
    
    @swagger_auto_schema(
        # operation_description="Получение рецепта по id",
        responses={200: MenuDataSerializer}
        )
    @action(methods=["POST"], detail=True, serializer_class=MenuRecipeIdSerializer)
    def generate_recipe(self, request, **kwargs):
        """ 
        Заменить позицию в меню (рецепт) на другой рецепт, \
            возвращает обновленное меню
        """
        recipe_id = request.data["recipe_id"]
        menu = self.get_object()
        menu_recipe = menu.menu_recipe.get(id=recipe_id)
        dislike = ResipesDislikes.objects.filter(user=request.user).values_list("recipe__id", flat=True)
        black_list = IngredientsBlacklist.objects.filter(user=request.user).values_list("ingredients_blacklist", flat=True)[0]
        recipe = Resipes.objects.exclude(id__in=dislike, ingredients__id__in=black_list).order_by("?").first()
        menu_recipe.recipe = recipe
        menu_recipe.save()
        menu_recipe_curent = {
            "id": menu.id, 
            "start_date": menu.start_date, 
            "end_date": menu.end_date,
            "recipes": [menu_recipe]
            }
        serializer = MenuDataSerializer({"data": {"menu":menu_recipe_curent}})
        return Response(serializer.data)
    
    
    @swagger_auto_schema(
        # operation_description="Получение рецепта по id",
        responses={200: MenuDataSerializer}
        )
    @action(methods=["POST"], detail=True, serializer_class=MenuRecipeIdSerializer)
    def remove_recipe(self, request, **kwargs):
        """ 
        Удаляет позицию в меню (рецепт), возвращает обновленное меню
        """
        recipe_id = request.data["recipe_id"]
        menu = self.get_object()
        recipe = menu.menu_recipe.filter(id=recipe_id).first()
        if not recipe:
            return Response({"status": "error", "detail": "recipe not found"})
        recipe.delete()
        likes = ResipesLikes.objects.filter(user=request.user).values_list("recipe__id", flat=True)
        dislike = ResipesDislikes.objects.filter(user=request.user).values_list("recipe__id", flat=True)
        black_list = IngredientsBlacklist.objects.filter(user=request.user).values_list("ingredients_blacklist", flat=True)[0]
        menu.generate_menu(likes, dislike, black_list)
        serializer = MenuDataSerializer({"data": {"menu":menu}})
        return Response(serializer.data)
    
    
    @action(methods=["GET"], detail=False, serializer_class=ShopListSerializer)
    def shop_list(self, request):
        """ 
        Возвращает список покупок для меню
        """
        menu = Menu.objects.filter(user=request.user, is_history=False).first()
        menu.shop_list_create_or_update()
        serializer = ShopListSerializer({"id": menu.id, "list": menu.shop_ingredients.all()})
        return Response(serializer.data)
    
    
    @swagger_auto_schema(responses={200: ShopListCheckedResponseSerializer})
    @action(methods=["POST"], detail=True, serializer_class=ShopListCheckedSerializer)
    def shop_list_checked(self, request, *args, **kwargs):
        """ 
        Изменеие состояния чекбоксов в списке покупок
        """
        cheked = request.data["cheked"]
        not_cheked = request.data["not_cheked"]
        menu = self.get_object()
        ingredients_checked = menu.shop_ingredients.filter(id__in=cheked)
        ingredients_checked.update(is_check=True)
        cheked_list = menu.shop_ingredients.filter(is_check=True).values_list("id", flat=True)
        ingredients_not_cheked = menu.shop_ingredients.filter(id__in=not_cheked)
        ingredients_not_cheked.update(is_check=False)
        not_cheked_list =  menu.shop_ingredients.filter(is_check=False).values_list("id", flat=True)
        serializer = ShopListCheckedResponseSerializer({"data": {"cheked": cheked_list, "not_cheked": not_cheked_list}})
        return Response(serializer.data)
    
    
    @action(methods=["GET"], detail=False)
    def history(self, request):
        """ 
        Возвращает историю меню
        """
        menu = Menu.objects.filter(user=request.user, is_history=True)
        serializer = MunuSerializer(menu, many=True)
        return Response({"status": "ok", "data": {"menu": serializer.data}})
    
