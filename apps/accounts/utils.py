import base64
import hashlib

from django.contrib.auth.models import User
from django.db import IntegrityError


def email_to_username(email):
    """
    Returns 30 char hashed version of an email, suitable for storage in Django's username field
    """
    email = email.lower()
    return base64.urlsafe_b64encode(hashlib.sha256(email).digest())[:30]


def create_user(email, password=None, is_staff=None, is_active=None):
    """
    Create a new user with the given email.
    Use this instead of `User.objects.create_user`.
    """
    try:
        username = email_to_username(email)
        user = User.objects.create_user(username, email, password)
    except IntegrityError, err:
        if err.message == 'column username is not unique':
            raise IntegrityError('user email is not unique')
        raise

    if is_active is not None or is_staff is not None:
        if is_active is not None:
            user.is_active = is_active
        if is_staff is not None:
            user.is_staff = is_staff
        user.save()
    return user