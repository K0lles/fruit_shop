from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password, **kwargs):
        username = AbstractBaseUser.normalize_username(username=username)
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.SlugField(unique=True)
    password = models.CharField(max_length=128)

    REQUIRED_FIELDS = ['username', 'password']

    USERNAME_FIELD = 'username'

    objects = UserManager()
