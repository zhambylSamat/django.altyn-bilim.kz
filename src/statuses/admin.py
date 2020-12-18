from django.contrib import admin
from .models import *


class GroupStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'description', 'is_active', 'created_date',
                          'updated_date', 'is_deleted')
    list_display_links = ('pk', )


admin.site.register(UserStatus)
admin.site.register(UserStatusHistory)
admin.site.register(GroupStatus)
admin.site.register(GroupStatusHistory, GroupStatusHistoryAdmin)
admin.site.register(LessonGroupStudentStatus)
admin.site.register(LessonGroupStudentStatusHistory)
