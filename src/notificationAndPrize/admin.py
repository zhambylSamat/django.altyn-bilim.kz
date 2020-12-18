from django.contrib import admin
from django.apps import apps
from .models import *


class NotificationAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'notification_type', 'notification_count', 'extra_object', 'extra_object_app_name',
                    'extra_object_model_name', 'main_object', 'object_app_name', 'object_model_name', 'is_shown',
                    'created_date')

    def extra_object(self, ent):
        invoice = apps.get_model(app_label=ent.extra_object_app_name, model_name=ent.extra_object_model_name)
        obj = invoice.objects.filter(pk=ent.extra_object_id).first()
        return obj

    def main_object(self, ent):
        invoice = apps.get_model(app_label=ent.object_app_name, model_name=ent.object_model_name)
        obj = invoice.objects.filter(pk=ent.object_id).first()
        return obj


admin.site.register(Notification, NotificationAdmin)
admin.site.register(Discount)
admin.site.register(Chocolate)
