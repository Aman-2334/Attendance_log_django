from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, registration=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        print(
            f"create user request with email {email} name {name} registration {registration}")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          registration=registration, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print(f"User Created: {user.email} {user.name} {user.registration}")
        return user

    def create_superuser(self, email, password=None, name=None, registration=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, name, registration, **extra_fields)
