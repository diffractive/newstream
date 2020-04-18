from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager


class User(BaseUser):
    is_email_verified = models.BooleanField(default=False)
    objects = BaseUserManager()
