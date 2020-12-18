from django.contrib import admin
from .models import *


class TeacherSalaryCategoryLevelAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'category', 'created_date')


class TeacherSalaryCategoryAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'teacher_salary_category_level', 'lessons_per_week', 'created_date')


class TeacherSalaryCoefficientAdmin(admin.ModelAdmin):
    list_display_links = ('pk', )
    list_display = ('pk', 'teacher_salary_category', 'coefficient', 'price')


class TeacherCategoryAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'teacher_salary_category_level', 'teacher', 'created_date')


admin.site.register(PreTeacherSalary)
admin.site.register(PreTeacherSalaryHistory)
admin.site.register(PostTeacherSalary)
admin.site.register(PostTeacherSalaryHistory)
admin.site.register(TeacherSalaryFile)
admin.site.register(TeacherSalaryCategory, TeacherSalaryCategoryAdmin)
admin.site.register(TeacherSalaryCategoryHistory)
admin.site.register(TeacherSalaryCoefficient, TeacherSalaryCoefficientAdmin)
admin.site.register(TeacherSalaryCoefficientHistory)
admin.site.register(TeacherCategory, TeacherCategoryAdmin)
admin.site.register(TeacherCategoryHistory)
admin.site.register(TeacherSalaryCategoryLevel, TeacherSalaryCategoryLevelAdmin)
admin.site.register(TeacherSalaryCategoryLevelHistory)
