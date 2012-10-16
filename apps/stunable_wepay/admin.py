#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.stunable_wepay.models import *


admin.site.register(WePayTransaction)

# class WePayTransactionAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(WePayTransaction, WePayTransactionAdmin)
