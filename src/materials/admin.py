from django.contrib import admin
from .models import *


class SubjectHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'created_user_id', 'title', 'created_date', 'updated_date', 'is_deleted')
    list_display_links = ('pk',)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'parent', 'title', 'is_endpoint', 'is_mid_control', 'order', 'created_date')
    list_display_links = ('pk',)
    search_fields = ('title',)


class TopicHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'created_user_id', 'subject_id', 'parent_id', 'title', 'is_endpoint',
                    'is_mid_control', 'order', 'created_date', 'updated_date', 'is_deleted')
    list_display_link = ('pk',)
    search_fields = ('title',)


class VideoAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'topic', 'title', 'duration', 'link', 'created_date')
    search_fields = ('topic__title', 'link')


class VideoHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'created_user_id', 'topic_id', 'title', 'duration', 'link', 'created_date',
                    'updated_date', 'is_deleted')
    list_display_links = ('pk',)


admin.site.register(Subject)
admin.site.register(SubjectHistory, SubjectHistoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicHistory, TopicHistoryAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(VideoHistory, VideoHistoryAdmin)
admin.site.register(TopicTest)
admin.site.register(TopicTestHistory)
admin.site.register(Question)
admin.site.register(QuestionHistory)
admin.site.register(Answer)
admin.site.register(AnswerHistory)
