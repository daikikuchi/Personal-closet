from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and Saves a new user"""
        if not email:
            raise ValueError('Please fill in email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and saves a super user"""
        admin_user = self.create_user(email, password)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save(using=self._db)

        return admin_user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """CustomUser model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
