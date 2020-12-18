from django.contrib.auth.models import User
from groupsAndLessons.models import (
    LessonGroup,
    LessonGroupHistory,
    GroupReplacement,
    LessonGroupStudentHistory,
    StudentPlanHistory,
    LessonGroupScheduleHistory,
    ScheduleHistory,
    DayOffHistory,
    GroupTimeTransferHistory,

)
from ..models import TeacherCategoryHistory, TeacherSalaryCategoryHistory, TeacherSalaryCoefficientHistory
from django.db.models import Q
from portal.api.utils import get_day_id_from_date, increase_one_day_in_date
from userInfo.models import StaffHistory
import math


def get_user_by_pk(user_pk):
    try:
        return User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return None


def get_student_user_by_pk(lesson_group_student_id):
    try:
        lesson_group_student = LessonGroupStudentHistory.objects.filter(origin_id=lesson_group_student_id).first()
        if lesson_group_student:
            student_plan = StudentPlanHistory.objects.filter(origin_id=lesson_group_student.student_plan_id).first()
            if student_plan:
                return User.objects.get(pk=student_plan.student_id)
        return None
    except User.DoesNotExist:
        return None


def get_lesson_group_by_id(group_pk):
    try:
        lesson_group = LessonGroup.objects.get(pk=group_pk)
        result = {
            'pk': lesson_group.pk,
            'title': lesson_group.title,
            'teacher': lesson_group.teacher,
            'is_deleted': False
        }
        return result
    except LessonGroup.DoesNotExist:
        lesson_group_history = LessonGroupHistory.objects.filter(origin_id=group_pk).order_by('-updated_date').first()
        result = {
            'pk': lesson_group_history.origin_id,
            'is_deleted': True,
            'title': lesson_group_history.title,
            'teacher': get_user_by_pk(lesson_group_history.teacher_id)
        }
        return result


def get_group_replacement(lesson_group_id, abs_date):
    try:
        return GroupReplacement.objects.get(Q(lesson_group__pk=lesson_group_id)
                                            & Q(date=abs_date))
    except GroupReplacement.DoesNotExist:
        return None


def get_all_lesson_days(lesson_group_id, start_date, finish_date): # date 31-01-2020
    lesson_group_schedule_list = LessonGroupScheduleHistory.objects.filter(lesson_group_id=lesson_group_id)
    result = []
    for ent in lesson_group_schedule_list:
        # from_date = ent.updated_date.date()
        date = start_date
        schedule = ScheduleHistory.objects.filter(origin_id=ent.schedule_id).first()
        while date <= finish_date:
            day_off_exists = False
            lesson_cancel_exists = False
            day_off = DayOffHistory.objects.filter(date=date).first()
            if day_off and not day_off.is_deleted:
                day_off_exists = True
            try:
                lesson_cancel = GroupReplacement.objects.get(Q(lesson_group_id=lesson_group_id)
                                                             & Q(date=date)
                                                             & Q(teacher__isnull=True))
                lesson_cancel_exists = True
            except GroupReplacement.DoesNotExist:
                pass

            if schedule.week_num == get_day_id_from_date(date)\
                    and not day_off_exists and not lesson_cancel_exists and date not in result:
                result.append(date)
            else:
                group_time_transfer = GroupTimeTransferHistory.objects.filter(Q(lesson_group_id=lesson_group_id)
                                                                              & Q(from_date=date)).first()
                if group_time_transfer and not group_time_transfer.is_deleted \
                        and group_time_transfer.to_date not in result:
                    result.append(group_time_transfer.to_date)
            date = increase_one_day_in_date(date)
    result.sort()
    return result


def get_teacher_category_by_schedule(lesson_group_id, user_id, coefficient):
    teacher = StaffHistory.objects.filter(user_id=user_id).first()
    lessons_per_week = LessonGroupScheduleHistory.objects.filter(lesson_group_id=lesson_group_id).count()
    teacher_category = TeacherCategoryHistory.objects.filter(teacher_id=teacher.origin_id).first()
    teacher_salary_category = TeacherSalaryCategoryHistory.objects.filter(
        Q(teacher_salary_category_level_id=teacher_category.teacher_salary_category_level_id)
        & Q(lessons_per_week=lessons_per_week)).first()
    teacher_salary_coefficient = TeacherSalaryCoefficientHistory.objects.filter(
        Q(teacher_salary_category_id=teacher_salary_category.origin_id)
        & Q(coefficient=coefficient)).first()
    if teacher_salary_coefficient:
        return float(teacher_salary_coefficient.price)
    return 0.00


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier
