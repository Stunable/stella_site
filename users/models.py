from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StellaUser(User):
    """A StellaUser is a subclass of django user, it provides the extra
    details that a user on ShopwithStella might have. 
    - Friends: The friends of this user. 
    - Closet: The user's closet. 
    """
    pass

class PotentialUser(models.Model):
    """A user that signs up for an invite. We need to store their email
    address and use it in the future for their account if they decide
    to sign-up. 
    """
    #email_address = models.charField()
