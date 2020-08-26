from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserMetrics(User):

    class Meta:
        proxy = True
        verbose_name = "User metics"
        verbose_name_plural = "User metrics"
