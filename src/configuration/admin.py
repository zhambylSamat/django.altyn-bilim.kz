from django.contrib import admin
from .models import *


class TrialTestMarkConfigurationAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'subject', 'max_mark', 'good_mark', 'bad_mark', 'created_date')


class SubjectQuizMarkConfigurationAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'subject', 'retake_mark', 'excellent_mark', 'created_date')


admin.site.register(TrialTestMarkConfiguration, TrialTestMarkConfigurationAdmin)
admin.site.register(TrialTestMarkConfigurationHistory)
admin.site.register(SubjectQuizConfiguration)
admin.site.register(SubjectQuizConfigurationHistory)
admin.site.register(LessonGroupIpConfiguration)
admin.site.register(LessonGroupIpConfigurationHistory)
admin.site.register(SubjectQuizMarkConfiguration, SubjectQuizMarkConfigurationAdmin)
admin.site.register(SubjectQuizMarkConfigurationHistory)
