from django.db import models
from django.conf import settings


class CourseLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    latitude = models.TextField(null=False, blank=False)
    longitude = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)
