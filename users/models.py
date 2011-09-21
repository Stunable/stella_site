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
