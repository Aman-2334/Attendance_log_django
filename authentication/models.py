from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .enums import RoleChoice
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    registration = models.CharField(max_length=255,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Role(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(max_length=255, choices=RoleChoice.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'role'], name='unique_user_role')
        ]

    def __str__(self):
        return f"{self.pk} {self.role}"

