from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.paginations import IngredientsPagination

from recepts.models import Ingredients, Resipes, ResipesIngredients
from recepts.serializer import *


class IngredientsViewSet(viewsets.GenericViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = SearchIngredientsSerializer
    pagination_class = IngredientsPagination

    
    @swagger_auto_schema(operation_description="Список ингридиентов с пагинацией. Фильтровать по query,"\
        "у каждого ингридиента будут ключевые слова, по которым и будет происходить поиск", 
        responses={200: IngredientsResponseSerializer()})
    def create(self, request):
        query = request.data.get('query')
        request.session['query'] = query
        queryset = Ingredients.objects.filter(
            Q(name__icontains=query))[:50]
        
        data = IngredientsSerializer(queryset, many=True).data
        page = self.paginate_queryset(data)
        if page:
            return self.get_paginated_response(page)
        result = IngredientsResponseSerializer({"data": {"list": queryset}})
        return Response(result.data)
    
    @swagger_auto_schema(operation_description="Список ингридиентов с пагинацией. Фильтровать по query,"\
        "у каждого ингридиента будут ключевые слова, по которым и будет происходить поиск", 
        responses={200: IngredientsResponseSerializer()})
    def list(self, request):
        queryset = self.queryset
        query = request.session.get('query')
        if query:
            queryset = Ingredients.objects.filter(
                Q(name__icontains=query))[:50]
        data = IngredientsSerializer(queryset, many=True).data
        page = self.paginate_queryset(data)
        if page:
            return self.get_paginated_response(page)
        result = IngredientsResponseSerializer({"data": {"list": queryset}})
        return Response(result.data)
    

class ResipesViewSet(viewsets.GenericViewSet):
    queryset = Resipes.objects.all()
    serializer_class = StatusReceptSerializer
    
    
    @swagger_auto_schema(
        operation_description="Получение рецепта по id",
        responses={200: StatusReceptSerializer}
        )
    def retrieve(self, request, *args, **kwargs):
        queryset = {"status": "ok", "data": Resipes.objects.get(id = kwargs['pk'])}
        serializer_data = self.get_serializer(queryset).data
        page = self.paginate_queryset(serializer_data)
        if page:
            return self.get_paginated_response(page)
        
        return Response(serializer_data)
