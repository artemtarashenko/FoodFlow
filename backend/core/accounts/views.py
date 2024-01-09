from django.conf import settings
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from accounts.models import CustomUser, OTP
from accounts.serializer import *
from recepts.serializer import IngredientsBlacklistGETSerializer, IngredientsBlacklistSerializer, \
    LikesDislikesSerializer, RecipeGETSerializer, RecipeSerializer
from recepts.models import IngredientsBlacklist, ResipesDislikes, ResipesLikes

from menu.models import MenuConfig

User = CustomUser

class RegistrationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationAuthSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegistrationAuthSerializer, 
        responses={
            200: StatusOkSerializer, 
            409: RegistrationStatusErrorSerializer, 
            410: RegistrationStatusWarningSerializer, 
            411: RegistrationStatusErrorSendSerializer})
    def create(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        code = OTP.generateOTP()

        user = User.objects.filter(email=email).first()
        if user is None:
            user = User.objects.create_user(email=email, name=name, password=password, is_active = False)
            otp = OTP(user=user, code=code)
            otp.save()
            try:
                send_mail(f'Одноразовый пароль для входа в личный кабинет: {email}', code, settings.EMAIL_HOST_USER, [email])
            except:
                return Response({"status": "error", "detail": "could_not_send_otp"}, status=411)
            
            result = {"status": "ok", "data": {"id": user.id, "email": user.email, "name": user.name, "code": otp.code}}
            status = 200
        elif not user.is_active:
            result = {"status": "warning", "detail": "otp_allredy_send"}
            status = 410
        else:    
            result = {"status": "error", "details": "allredy_registered"}
            status = 409

        return Response(result, status)

    
    @swagger_auto_schema(
        request_body=ConfirmUserSerializer, 
        responses={200: StatusOkUserSerializer, 400: ConfirmStatusErrorUserSerializer})
    @action(detail=False, methods=['POST'], serializer_class=ConfirmUserSerializer)
    def confirmation(self, request):
        code = request.data.get('code')
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        otp = OTP.objects.filter(user=user).first()
        if otp.code == code:
            otp.code = ""
            otp.save()
            user.is_active = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            result = {
                "status": "ok",
                "data": {
                    "token": f'Token {token.key}',
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                    }
                }
            }
            status = 200
        else:
            result = {"status": "error", "detail": "wrong_confirm_code"}
            status = 400

        return Response(result, status=status)

    
    @swagger_auto_schema(
        request_body=ConfirmUserResendSerializer, 
        responses={200: StatusOkSerializer})
    @action(detail=False, methods=['POST'], serializer_class=ConfirmUserResendSerializer)
    def resend_confirm(self, request):
        email = request.data.get('email')
        resend = request.data.get('resend')
        if resend and email:
            code = OTP.generateOTP()
            user = User.objects.filter(email=email).first()
            otp = OTP.objects.filter(user=user).first()
            otp.code = code
            otp.save()
            send_mail(f'Одноразовый пароль для входа в личный кабинет: {email}', code, settings.EMAIL_HOST_USER,
                      [email])
            result = {"status": "ok"}
            return Response(result)

class UserAuthTokenViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: StatusOkUserSerializer, 
            401: StatusErrorNotRegUserSerializer,
            402: StatusErrorWrongPasswordUserSerializer
            }
        )
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is not None:
            check_password = user.check_password(password)
            if check_password:
                token, created = Token.objects.get_or_create(user=user)
                result = StatusOkUserSerializer({"data": {"user": user, "token": f"Token {token}"}}).data
                status = 200
            else:
                result = {"status": "error", "details": "wrong_password"}
                status = 402
                
        else:
            result = {"status": "error", "details": "not_registrated"}
            status = 401

        return Response(result, status=status)
    
    @swagger_auto_schema(
        responses={
            200: StatusOkSerializer, 
            410: StatusErrorNotRegUserSerializer,
            409: ConfirmStatusErrorUserSerializer,
            411: ResendPassStatusErrorSerializer
            }
        )
    @action(methods=["POST"], detail=False, serializer_class=UserResendPasswordSerializer)
    def resend_password(self, request):
        code = request.data.get('code')
        email = request.data.get('email')
        password = request.data.get('password')
        
        fields = ["code","email","password"]
        not_fields = [field for field in fields if not request.data.get(field)]
        
        if len(not_fields) > 0:
            return Response({"status": "error", "detail": f"not_fields {not_fields}"}, status=411)
        
        user = User.objects.filter(email=email).first()
        if user:
            otp = OTP.objects.filter(user=user).first()
            if otp.code == code:
                user.set_password(password)
                user.save()
                result = {"status": "ok"}
                status = 200
            else:
                result = {"status": "error", "detail": "wrong_confirm_code"}
                status = 409
        else:
            result = {"status": "error", "detail": "not_registrated"}
            status = 410
        
        return Response(result, status=status)
        

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserPostSerializer
    
    user_response = openapi.Response('Данные пользователя', UserResponseSerializer)
    @swagger_auto_schema(request_body=UserPostSerializer, responses={200: user_response})
    def create(self, request):
        """
        изменение данных, все поля необязательные
        """
        name = request.data.get("name")
        meal_count = request.data.get("meal_count")
        portions_count = request.data.get("portions_count")
        
        user = request.user
        if name != "":
            user.name = name 
            user.save()
        
        menu_config = MenuConfig.objects.filter(user=user).first()
        if menu_config is not None:
            menu_config.meal_count = meal_count if meal_count != "" else menu_config.meal_count
            menu_config.portions_count = portions_count if portions_count != "" else menu_config.portions_count
            menu_config.save()
        else:
            menu_config = MenuConfig(
                user=user, 
                meal_count=meal_count if meal_count != "" else 0, 
                portions_count=portions_count if portions_count != "" else 0
                )
            menu_config.save()
        
        result = {"status": "ok", "data": UserSerializer(user).data}
        
        return Response(result)
    
    @swagger_auto_schema(responses={200: UserResponseSerializer})
    def list(self, request):
        """
        данние пользователя
        """
        user = request.user
        result = {
            "status": "ok",
            "data": UserSerializer(user).data
        }
        return Response(result)

    @swagger_auto_schema(responses={200: StatusOkSerializer})
    @action(methods=["DELETE"], detail=False)
    def delete(self, request):
        """удаление акка и всё что с ним связанно"""
        user = request.user
        user.delete()
        result = {"status": "ok"}
        return Response(result)


    @swagger_auto_schema(request_body=LikesDislikesSerializer, responses={200: StatusOkSerializer})
    @action(methods=["POST"], detail=False, serializer_class=LikesDislikesSerializer)
    def like(self, request):
        """
        добавление указанного id в likes пользователя. 
        Если указанный id уже есть в likes - убирает этот id из likes
        """
        recipe_id = request.data["id"]
        user = request.user
        like = ResipesLikes.objects.filter(user=user, recipe__id=recipe_id).first()
        if like is None:
            like = ResipesLikes(user=user, recipe_id=recipe_id)
            like.save()
        else:
            like.delete()
        
        result = {"status": "ok"}
        return Response(result)
    
    
    @swagger_auto_schema(responses={200: RecipeGETSerializer})
    @action(methods=["GET"], detail=False, serializer_class=RecipeGETSerializer)
    def like_get(self, request):
        user = request.user
        likes = ResipesLikes.objects.filter(user=user)
        likes_resipes = [x.recipe for x in likes]
        result = {"status": "ok", "data": {"resipes": RecipeSerializer(likes_resipes, many=True).data}}
        
        return Response(result)
    
    
    @swagger_auto_schema(request_body=LikesDislikesSerializer, responses={200: StatusOkSerializer})
    @action(methods=["POST"], detail=False, serializer_class=LikesDislikesSerializer)
    def dislike(self, request):
        """
        добавление указанного id в dislikes пользователя. 
        Если указанный id уже есть в dislikes - убирает этот id из dislikes
        """
        recipe_id = request.data["id"]
        user = request.user
        like = ResipesDislikes.objects.filter(user=user, recipe__id=recipe_id).first()
        if like is None:
            like = ResipesDislikes(user=user, recipe_id=recipe_id)
            like.save()
        else:
            like.delete()
        
        result = {"status": "ok"}
        
        return Response(result)
    
    @swagger_auto_schema(responses={200: RecipeGETSerializer})
    @action(methods=["GET"], detail=False, serializer_class=RecipeGETSerializer)
    def dislike_get(self, request):
        user = request.user
        dislike = ResipesDislikes.objects.filter(user=user)
        dislike_resipes = [x.recipe for x in dislike]
        result = {"status": "ok", "data": {"resipes": RecipeSerializer(dislike_resipes, many=True).data}}
        
        return Response(result)
    
    
    @swagger_auto_schema(request_body=IngredientsBlacklistSerializer, responses={200: StatusOkSerializer})
    @action(methods=["POST"], detail=False, serializer_class=IngredientsBlacklistSerializer)
    def black_list(self, request):
        """
        изменяет блэклист ингредиентов
        """
        ingredients_blacklist = request.data.get("ingredients_blacklist")
        user = request.user
        
        ingredient_blacklist = IngredientsBlacklist.objects.filter(user=user).first()
        if ingredient_blacklist is not None:
            ingredient_blacklist.ingredients_blacklist = ingredients_blacklist
        else:
            ingredient_blacklist = IngredientsBlacklist(user=user, ingredients_blacklist = ingredients_blacklist)
            ingredient_blacklist.save()

        result = {"status": "ok"}
        
        return Response(result)
    
    
    @swagger_auto_schema(responses={200: IngredientsBlacklistGETSerializer})
    @action(methods=["GET"], detail=False, serializer_class=IngredientsBlacklistGETSerializer)
    def black_list_get(self, request):
        user = request.user
        ingredient_blacklist = IngredientsBlacklist.objects.filter(user=user).first()
        serializer = IngredientsBlacklistGETSerializer({"data":ingredient_blacklist})
        
        return Response(serializer.data)
    