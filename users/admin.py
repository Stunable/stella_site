import models
from django.contrib import admin

"""Registers the users app with the django admin interface.
"""

admin.site.register(models.StellaUser)
