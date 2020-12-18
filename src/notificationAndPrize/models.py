from django.db import models
from .api.constants import NOTIFICATION_TYPE, NOTIFICATION_CLASS
from django.conf import settings


class Notification(models.Model):
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE)
    notification_class = models.CharField(max_length=1, choices=NOTIFICATION_CLASS)
    notification_count = models.IntegerField()
    extra_object_id = models.IntegerField()
    extra_object_app_name = models.CharField(max_length=120)
    extra_object_model_name = models.CharField(max_length=120)
    object_id = models.IntegerField()
    object_app_name = models.CharField(max_length=120)
    object_model_name = models.CharField(max_length=120)
    is_shown = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


class Discount(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT)
    is_got = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


class Chocolate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT)
    is_got = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
