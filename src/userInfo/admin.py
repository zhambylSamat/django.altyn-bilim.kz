from django.contrib import admin
from .models import *


class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'has_payment', 'has_contract', 'is_password_reset', 'gender', 'grade', 'phone',
                    'certificate', 'dob', 'school', 'home_phone', 'address', 'target_subject', 'instagram',
                    'force_access_until', 'created_date')
    list_display_links = ('pk',)
    search_fields = ('phone', 'user__username')


class StudentHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'user_id', 'has_payment', 'has_contract', 'is_password_reset', 'gender',
                    'phone', 'certificate', 'dob', 'school', 'home_phone', 'address', 'target_subject', 'target_from',
                    'instagram', 'force_access_until', 'created_date', 'updated_date', 'is_deleted', 'changed_user_id')
    list_display_links = ('pk',)


class ParentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'student', 'is_main', 'phone', 'created_date')
    list_display_links = ('pk', )


class ParentHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'user_id', 'changed_user_id', 'student_id', 'is_main',
                    'phone', 'created_date', 'updated_date', 'is_deleted')
    list_display_links = ('pk', )


class StaffAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'dob', 'is_password_reset', 'created_date')
    list_display_links = ('pk', )


class StaffHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'user_id', 'changed_user_id', 'dob', 'is_password_reset', 'created_date',
                    'updated_date', 'is_deleted')
    list_display_links = ('pk',)


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'role')
    list_display_links = ('pk',)


class UserRoleHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin_id', 'user_id', 'role', 'updated_date', 'is_deleted')
    list_display_links = ('pk',)


admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserRoleHistory, UserRoleHistoryAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentHistory, StudentHistoryAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(ParentHistory, ParentHistoryAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(StaffHistory, StaffHistoryAdmin)
admin.site.register(StudentFreeze)
admin.site.register(StudentFreezeHistory)
admin.site.register(StudentGroupFreeze)
admin.site.register(StudentGroupFreezeHistory)
