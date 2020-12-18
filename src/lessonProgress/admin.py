from django.contrib import admin
from .models import *


class GroupStudentVisitAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'lesson_group', 'abs_date', 'created_date')


class GroupStudentVisitHistoryAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'origin_id', 'changed_user_id', 'lesson_group_id', 'abs_date', 'created_date', 'updated_date',
                    'is_delete')


class StudentVisitAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'group_student_visit', 'lesson_group_student', 'attendance', 'home_work', 'no_home_work')
    search_fields = ('lesson_group_student__student_plan__student__last_name',
                     'lesson_group_student__student_plan__student__first_name',)


class StudentVisitHistoryAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'origin_id', 'changed_user_id', 'group_student_visit_id', 'lesson_group_student_id', 'attendance', 'home_work', 'no_home_work', 'updated_date', 'is_deleted')


class TrialTestAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'student', 'subject')
    search_fields = ('student__username', 'subject__title')


class TrialTestHistoryAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'origin_id', 'changed_user_id', 'student_id', 'subject_id', 'updated_date', 'is_deleted')


class TopicQuizMarkAdmin(admin.ModelAdmin):
    list_display_link = ('pk',)
    list_display = ('pk', 'topic_plan', 'practice', 'theory', 'created_date')


class TopicQuizMarkHistoryAdmin(admin.ModelAdmin):
    list_display_link = ('pk',)
    list_display = ('pk', 'origin_id', 'changed_user_id', 'topic_plan_id', 'practice', 'theory', 'created_date')


class TrialTestMarkAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'trial_test', 'mark', 'date', 'created_date')


class TrialTestMarkHistoryAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'origin_id', 'changed_user_id', 'trial_test_id', 'mark', 'date', 'created_date',
                    'updated_date', 'is_deleted')


admin.site.register(TopicQuizMark, TopicQuizMarkAdmin)
admin.site.register(TopicQuizMarkHistory, TopicQuizMarkHistoryAdmin)
admin.site.register(GroupStudentVisit, GroupStudentVisitAdmin)
admin.site.register(GroupStudentVisitHistory, GroupStudentVisitHistoryAdmin)
admin.site.register(StudentVisit, StudentVisitAdmin)
admin.site.register(StudentVisitHistory, StudentVisitHistoryAdmin)
admin.site.register(TrialTest, TrialTestAdmin)
admin.site.register(TrialTestHistory, TrialTestHistoryAdmin)
admin.site.register(TrialTestMark, TrialTestMarkAdmin)
admin.site.register(TrialTestMarkHistory, TrialTestMarkHistoryAdmin)
admin.site.register(LessonVideoAction)
admin.site.register(LessonVideoActionHistory)
admin.site.register(LessonTestAction)
admin.site.register(LessonTestActionHistory)
