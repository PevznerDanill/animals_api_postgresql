from django.db import models
from django.contrib.auth.models import AbstractUser
from app_animals.models import Shelter


class User(AbstractUser):
    """
    Extends the default User model. Adds the fields shelter (ForeignKey to Shelter model),
    is_guest and asked_for_upgrade.
    """
    shelter = models.ForeignKey(to=Shelter, related_name='users', on_delete=models.CASCADE, null=True)
    is_guest = models.BooleanField(default=True)
    asked_for_upgrade = models.BooleanField(default=False)
