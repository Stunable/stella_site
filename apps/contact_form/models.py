from django.db import models

class Contact(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField()
    message = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
