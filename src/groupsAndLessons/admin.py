from django.contrib import admin
from .models import *


class StudentPlanAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'student', 'subject', 'progress', 'created_date')
    search_fields = ('student__username', 'subject__title')


class SubjectPlanAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'student_plan', 'subject', 'created_date')


class StudentPlanHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'student_id', 'subject_id', 'progress', 'created_date',
                    'updated_date', 'is_deleted')
    list_display_links = ('pk',)


class SubjectPlanHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'student_plan_id', 'subject_id', 'created_date',
                    'updated_date', 'is_deleted')
    list_display_links = ('pk',)


class TopicPlanHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'subject_plan_id', 'topic_id', 'tutorial', 'class_work',
                    'home_work', 'created_date', 'updated_date', 'is_deleted')
    list_display_links = ('pk',)


class OfficeHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'title', 'created_date', 'updated_date', 'is_deleted')
    list_display_links = ('pk',)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'office_id', 'week_num', 'start_time', 'finish_time', 'created_date')
    list_display_links = ('pk', )


class ScheduleHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'office_id', 'week_num', 'start_time', 'finish_time',
                    'created_date', 'updated_date', 'is_deleted')
    list_display_links = ('pk', )


class LessonGroupHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'teacher_id', 'title', 'student_limit',
                    'send_message_on_no_payment', 'created_date', 'updated_date', 'is_deleted')
    list_display_links = ('pk',)


class LessonGroupScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'schedule', 'group_schedule')
    list_display_links = ('pk',)


class LessonGroupScheduleHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'schedule_id', 'group_schedule_id', 'updated_date',
                    'is_deleted')
    list_display_links = ('pk',)


class GroupReplacementAdmin(admin.ModelAdmin):
    list_display = ('pk', 'lesson_group', 'teacher', 'date', 'created_date')
    list_display_links = ('pk',)


class GroupReplacementHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'changed_user_id', 'lesson_group_id', 'teacher_id', 'date', 'created_date',
                    'updated_date', 'is_deleted')
    list_display_links = ('pk',)


admin.site.register(Office)
admin.site.register(OfficeHistory, OfficeHistoryAdmin)
admin.site.register(GroupSchedule)
admin.site.register(GroupScheduleHistory)
admin.site.register(LessonGroupSchedule, LessonGroupScheduleAdmin)
admin.site.register(LessonGroupScheduleHistory, LessonGroupScheduleHistoryAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(ScheduleHistory, ScheduleHistoryAdmin)
admin.site.register(LessonGroup)
admin.site.register(LessonGroupHistory, LessonGroupHistoryAdmin)
admin.site.register(StudentPlan, StudentPlanAdmin)
admin.site.register(StudentPlanHistory, StudentPlanHistoryAdmin)
admin.site.register(SubjectPlan, SubjectPlanAdmin)
admin.site.register(SubjectPlanHistory, SubjectPlanHistoryAdmin)
admin.site.register(TopicPlan)
admin.site.register(TopicPlanHistory, TopicPlanHistoryAdmin)
admin.site.register(LessonGroupStudent)
admin.site.register(LessonGroupStudentHistory)
admin.site.register(MaterialAccessInfo)
admin.site.register(MaterialAccessInfoHistory)
admin.site.register(GroupReplacement, GroupReplacementAdmin)
admin.site.register(GroupReplacementHistory, GroupReplacementHistoryAdmin)
admin.site.register(LessonGroupStudentShortSchedule)
admin.site.register(LessonGroupStudentShortScheduleHistory)
admin.site.register(DayOff)
admin.site.register(DayOffHistory)
admin.site.register(GroupTimeTransfer)
admin.site.register(GroupTimeTransferHistory)
