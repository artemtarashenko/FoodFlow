from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import MenuConfig

User = get_user_model()

class MunuConfigSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuConfig
        fields = ["meal_count", "portions_count"]