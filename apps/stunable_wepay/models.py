from django.db import models
from django.contrib.auth.models import User


class WePayTransaction(models.Model):
    checkout_id = models.CharField(max_length=128)
    state = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now_add=True)
