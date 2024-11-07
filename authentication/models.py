from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser

from .manager import UserManager
from institution.models import Institution


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    registration = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Role(models.Model):
    role = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.role


class User_Role(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userRoles_user')
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='userRoles_role')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'], name='unique_user_role')
        ]

    def __str__(self):
        return f"{self.user} {self.role}"


class User_Institute(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='UserInstitute_user')
    institute = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name='UserInstitute_institute')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'institute'], name='unique_user_institute')
        ]

    def __str__(self):
        return f"{self.user} {self.role}"
