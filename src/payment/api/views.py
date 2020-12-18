from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from portal.api.utils import permission
import datetime
from django.db.models import Q

from portal.api.constants import DEVELOPER_ROLE, ADMIN_ROLE
from lessonProgress.models import GroupStudentVisitHistory, StudentVisitHistory
from .utils import (
    get_lesson_group_by_id,
    get_group_replacement,
    get_student_user_by_pk,
    get_all_lesson_days,
    round_half_up,
    get_teacher_category_by_schedule
)
import calendar
from ..models import PreTeacherSalary


# class ResponseThen(Response):
#     def __init__(self, data, then_callback, month, year, user, **kwargs):
#         super().__init__(data, **kwargs)
#         self.then_callback = then_callback
#         self.month = month
#         self.year = year
#         self.user = user
#
#     def close(self):
#         super().close()
#         self.then_callback(self.month, self.year, self.user)


class GroupListForSalaryCalculations(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, month, year):
        roles = (DEVELOPER_ROLE, ADMIN_ROLE)
        permission(roles, request.user)

        group_student_visit_list = GroupStudentVisitHistory.objects.filter(Q(abs_date__month=month)
                                                                           & Q(abs_date__year=year)) \
                                                                           .order_by('lesson_group_id', 'abs_date')
        result = []
        for ent in group_student_visit_list:
            if ent.lesson_group_id not in result:
                result.append(ent.lesson_group_id)
        return Response(result, status=200)


class CalculateSalaryListView(APIView):

    # permission_classes = (AllowAny,)
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, month, year, lesson_group_id):
        roles = (DEVELOPER_ROLE, ADMIN_ROLE)
        permission(roles, request.user)
        # return ResponseThen({'result': 'success'}, self.do_calculation, month, year, request.user, status=200)

        group_student_visit_list = GroupStudentVisitHistory.objects.filter(Q(abs_date__month=month)
                                                                           & Q(abs_date__year=year)) \
            .order_by('lesson_group_id', 'abs_date')
        month_range = calendar.monthrange(int(year), int(month))
        last_day_of_lesson = datetime.datetime.strptime('{}-{}-{}'.format(year, month, month_range[1]), '%Y-%m-%d')
        last_day_of_lesson = last_day_of_lesson.date()
        first_date_of_lesson = last_day_of_lesson.replace(day=1)

        group_result = {}
        student_result = {}
        for group_visit_ent in group_student_visit_list:
            lesson_group = get_lesson_group_by_id(group_visit_ent.lesson_group_id)
            group_replacement = get_group_replacement(lesson_group['pk'], group_visit_ent.abs_date)
            if group_replacement:
                teacher = group_replacement.teacher.user
            else:
                teacher = lesson_group['teacher']
            if teacher.pk not in group_result:
                group_result[teacher.pk] = {
                    'pk': teacher.pk,
                    'last_name': teacher.last_name,
                    'first_name': teacher.first_name,
                    'groups': {},
                    'total_salary': 0.0
                }

            if lesson_group['pk'] not in group_result[teacher.pk]['groups']:
                all_taught_days = get_all_lesson_days(lesson_group['pk'], first_date_of_lesson, last_day_of_lesson)
                group_result[teacher.pk]['groups'][lesson_group['pk']] = {
                    'title': lesson_group['title'],
                    'log': {},
                    'students_count': 0,
                    'student_coefficient': {},
                    'total_student_coefficient': 0.0,
                    'all_lesson_days': [str(item) for item in all_taught_days],
                    'all_lesson_day_count': len(all_taught_days),
                    'all_taught_days': [],
                    'all_taught_day_count': 0,
                    'pre_salary': 0.00,
                    'salary': 0.00,
                }
            link_to_group = group_result[teacher.pk]['groups'][lesson_group['pk']]
            link_to_group['all_taught_days'].append(str(group_visit_ent.abs_date))
            link_to_group['all_taught_day_count'] += 1
            tmp = {
                'abs_date': str(group_visit_ent.abs_date),
                'has_replacement': True if group_replacement else False,
                'students': {}
            }
            link_to_group['log'][group_visit_ent.origin_id] = tmp
            student_visit_list = StudentVisitHistory.objects.filter(group_student_visit_id=group_visit_ent.origin_id)
            for student_visit_ent in student_visit_list:
                student = get_student_user_by_pk(student_visit_ent.lesson_group_student_id)
                if student.pk not in student_result:
                    student_result[student.pk] = {
                        'pk': student.pk,
                        'last_name': student.last_name,
                        'first_name': student.first_name
                    }
                link_to_group['log'][group_visit_ent.origin_id]['students'][student.pk] = {
                    'pk': student.pk,
                    'last_name': student.last_name,
                    'first_name': student.first_name,
                    'attendances': student_visit_ent.attendance
                }
                all_taught_days = link_to_group['all_lesson_day_count']
                if student.pk not in link_to_group['student_coefficient']:
                    link_to_group['students_count'] += 1
                    link_to_group['student_coefficient'][student.pk] = {
                        'count': 1,
                        'coefficient': round_half_up(1 / all_taught_days, 1)
                    }
                else:
                    link_to_group['student_coefficient'][student.pk]['count'] += 1
                    count = link_to_group['student_coefficient'][student.pk]['count']
                    link_to_group['student_coefficient'][student.pk]['coefficient'] = round_half_up(
                        count / all_taught_days, 1)
            tmp_total_coefficient = 0.0
            for key, val in link_to_group['student_coefficient'].items():
                tmp_total_coefficient += val['coefficient']
            tmp_total_coefficient = round_half_up(tmp_total_coefficient, 1)
            link_to_group['total_student_coefficient'] = tmp_total_coefficient
            pre_salary = get_teacher_category_by_schedule(lesson_group['pk'],
                                                          lesson_group['teacher'].pk,
                                                          tmp_total_coefficient)
            link_to_group['pre_salary'] = pre_salary
            salary = (link_to_group['all_taught_day_count'] / link_to_group['all_lesson_day_count']) * pre_salary
            link_to_group['salary'] = round(salary, 2)
        for teacher_key, teacher_val in group_result.items():
            for group_key, group_val in teacher_val['groups'].items():
                teacher_val['total_salary'] += group_val['salary']

        total_result = {
            'teachers': group_result,
            'students': student_result
        }
        return Response(total_result, status=200)


# class TmpSetTeacherSalaryCoefficientView(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request, teacher_salary_category_pk):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#
#         try:
#             teacher_salary_category = TeacherSalaryCategory.objects.get(pk=teacher_salary_category_pk)
#             coefficient = 0.0
#             for item in request.data:
#                 coefficient += 0.1
#                 teacher_salary_coefficient = TeacherSalaryCoefficient(teacher_salary_category=teacher_salary_category,
#                                                                       coefficient=coefficient,
#                                                                       price=item)
#                 teacher_salary_coefficient.save(user_pk=request.user.pk)
#             return Response(status=201)
#         except TeacherSalaryCategory.DoesNotExist:
#             return Response(status=404)

