from django.db import models
from django.contrib.auth.models import User

from .enums import RoleChoice

# class Firebase_userID(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     firebase_id = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return f"{self.user.pk} {self.user.email} - {self.firebase_id}"


class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=RoleChoice.choices)

    def __str__(self):
        return f"{self.user.pk} {self.user.email} - {self.role}"
