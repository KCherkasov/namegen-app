# -**- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CharsheetUserManager(BaseUserManager):
    def all(self):
        return super(CharsheetUserManager, self).all()

    def create_user(self, id, email, is_master, password=None):
        if not email:
            raise ValueError('Необходимо ввести email')
        email = self.normalize_email(email)
        user = self.model(id, self.normalize_email(email), is_master)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, is_master, password=None):
        user = self.create_user(id, email, is_master, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CharsheetUser(AbstractBaseUser):
    id = models.CharField(verbose_name=u'Логин',max_length=40, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    is_master = models.BooleanField(verbose_name=u'Мастер', default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CharsheetUserManager()

    USERNAME_FIELD = 'id'
    EMAIL_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin