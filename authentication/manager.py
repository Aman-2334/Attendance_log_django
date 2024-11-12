from django.contrib.auth.models import BaseUserManager
from institution.models import Institution


class UserManager(BaseUserManager):
    def create_user(self, email, role, institute, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        if not role:
            raise ValueError('The role field must be set')
        if not institute:
            raise ValueError('The institute field must be set')
        print(
            f"create user request with email {email} name {name}")
        from authentication.models import Role
        try:
            role_instance = Role.objects.get(id=role)
        except Role.DoesNotExist:
            raise ValueError(f"Role with id {role} does not exist")
        try:
            institute_instance = Institution.objects.get(id=institute) 
        except Institution.DoesNotExist:
            raise ValueError(f"Institution with id {institute} does not exist")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role = role_instance, institute = institute_instance, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print(f"User Created: {user.email} {user.name}")
        return user

    def create_superuser(self, email, role, institute, password=None, name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, role, institute, password, name, **extra_fields)
