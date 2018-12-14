from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    homePage = models.CharField(max_length=10, null=True)
    date =  models.DateTimeField(default=timezone.now())