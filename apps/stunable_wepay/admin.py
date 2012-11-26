#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.stunable_wepay.models import *


class WePayTransactionAdmin(admin.ModelAdmin):
    actions = ('capture_funds',)

    def capture_funds(self,request,queryset):
        for obj in queryset:
            obj.capture_funds()
#     pass
admin.site.register(WePayTransaction, WePayTransactionAdmin)
