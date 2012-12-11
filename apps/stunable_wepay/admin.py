#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.stunable_wepay.models import *


class WePayTransactionAdmin(admin.ModelAdmin):
    list_display = ('state','checkout_id','date_created')
    actions = ('capture_funds','get_wepay_status')

    def capture_funds(self,request,queryset):
        for obj in queryset:
            obj.capture_funds()

    def get_wepay_status(self,request,queryset):
        for obj in queryset:
            obj.get_status()
#     pass
admin.site.register(WePayTransaction, WePayTransactionAdmin)
