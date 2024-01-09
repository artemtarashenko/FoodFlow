import math
import random

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='Пользователь', blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(verbose_name="Проверочный код", max_length=255, blank=True, null=True)

    @classmethod
    def generateOTP(cls):
        """Генератор случайных чисел"""
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP