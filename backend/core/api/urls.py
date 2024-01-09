from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import RegistrationViewSet, UserAuthTokenViewSet, UserViewSet
from menu.views import MenuViewSet
from recepts.views import IngredientsViewSet, ResipesViewSet

router = DefaultRouter()
router.register(r'v1/registration', RegistrationViewSet, basename="registration")
router.register(r'v1/auth', UserAuthTokenViewSet, basename="auth")
router.register(r'v1/user', UserViewSet, basename="user")
router.register(r'v1/resipes', ResipesViewSet, basename="resipes")
router.register(r'v1/ingredients', IngredientsViewSet, basename="ingredients")
router.register(r'v1/menu', MenuViewSet, basename="menu")

#v2
# router.register(r'v2/ingredients', IngredientsViewSet, basename="v2_ingredients")

urlpatterns = [
    path('', include(router.urls)),
]
