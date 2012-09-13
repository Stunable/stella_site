from django.contrib.auth.models import User
from django.db.models import Q

class EmailAuthenticationBackend(object):
    """
    Authenticate the user by email and password.
    
    django.contrib.auth.models.User does not force unique emails, so this
    backend will try to authenticate all users that match the given email,
    and return the first successfully authenticated user.
    """
    def authenticate(self, email=None, password=None):
        username_or_email = Q(username=email) | Q(email=email)
        try:
            for user in User.objects.filter(username_or_email, is_active=True):
                if user.check_password(password):
                    user.backend = "%s.%s" % (self.__module__, self.__class__.__name__)
                    return user
        except:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None