from rest_framework import serializers
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser

from menu.serializer import MunuConfigSerializer

User = CustomUser


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class UserResendPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    code = serializers.CharField()
    
class ResendPassStatusErrorSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='error')
    detail = serializers.CharField(max_length=200, default='not_fields []')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    menu_config = MunuConfigSerializer()
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'menu_config']
        
class UserResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='ok')
    data = UserSerializer()

class UserPostSerializer(serializers.ModelSerializer):
    meal_count = serializers.IntegerField(source="menu_config.meal_count")
    portions_count = serializers.IntegerField(source="menu_config.portions_count")
    
    class Meta:
        model = User
        fields = ['name', 'meal_count', 'portions_count']

class TokenUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()
        
class StatusOkUserSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='ok')
    data = TokenUserSerializer()
    
class StatusErrorNotRegUserSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='error')
    detail = serializers.CharField(max_length=200, default='not_registrated')

class StatusErrorWrongPasswordUserSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='error')
    detail = serializers.CharField(max_length=200, default='wrong_password')

"""Registration"""
class RegistrationAuthSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']

class RegistrationStatusErrorSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='error')
    detail = serializers.CharField(max_length=200, default='allredy_registered')
    
class RegistrationStatusWarningSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='warning')
    detail = serializers.CharField(max_length=200, default='otp_allredy_send')
    
class RegistrationStatusErrorSendSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='error')
    detail = serializers.CharField(max_length=200, default='could_not_send_otp')

"""Confirm"""
class ConfirmUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=6)

class ConfirmUserResendSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    resend = serializers.BooleanField()
        
class ConfirmStatusErrorUserSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='error')
    detail = serializers.CharField(max_length=200, default='wrong_confirm_code')

"""status"""
class StatusOkSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, default='ok')
