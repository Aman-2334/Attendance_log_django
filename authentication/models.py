from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .manager import UserManager
from institution.models import Institution

class Role(models.Model):
    role = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.role

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    registration = models.CharField(max_length=255, blank=True)
    role = models.ForeignKey(Role,on_delete=models.DO_NOTHING)
    institute = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','role','institute']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email