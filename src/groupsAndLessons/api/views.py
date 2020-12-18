from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from portal.api.utils import permission
import datetime
from django.db.models import Q

from portal.api.constants import (
    DEVELOPER_ROLE,
    ADMIN_ROLE,
    SUPER_MODERATOR_ROLE,
    MODERATOR_ROLE,
    FULL_STAFF_ROLES,
    TEACHER_ROLE,
    WEEK_DAY_SHORT_CHOICES_LIST
)
from ..models import (
    StudentPlan,
    Office,
    Schedule,
    LessonGroup,
    LessonGroupSchedule,
    LessonGroupStudent,
    GroupReplacement,
    LessonGroupStudentShortSchedule,
    DayOff,
    GroupTimeTransfer,
    GroupSchedule,
    MaterialAccessInfo
)
from .serializer import (
    StudentSubjectTopicSerializer,
    OfficeSerializer,
    ScheduleSerializer,
    LessonGroupWithScheduleSerializers,
    LessonGroupStudentSerializer,
    LessonGroupFullSerializer,
    GroupReplacementSerializer,
    LessonGroupStudentShortScheduleSerializer,
    DayOffSerializer,
    GroupTimeTransferSerializer
)
from lessonProgress.api.utils import set_ip
from portal.api.utils import delete_ent, delete_ent_list


class StudentPlanDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, student_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        student_plan = StudentPlan.objects.filter(student__pk=student_pk)
        if student_plan:
            student_plan_serializer = StudentSubjectTopicSerializer(student_plan, many=True)
            return Response(student_plan_serializer.data, status=200)
        else:
            return Response([], status=200)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        student_subject_topic_serializer = StudentSubjectTopicSerializer(data=request.data.copy())
        error_message = {'message': []}
        if student_subject_topic_serializer.is_valid():
            student_plan = student_subject_topic_serializer.save(user_pk=request.user.pk)
            student_plan_serializer = StudentSubjectTopicSerializer(student_plan)
            return Response(student_plan_serializer.data, status=201)
        else:
            error_message['message'].append(student_subject_topic_serializer.errors)
            return Response(error_message, status=206)

    def put(self, request, student_plan_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        student_plan = StudentPlan.objects.get(pk=student_plan_pk)
        student_subject_topic_serializer = StudentSubjectTopicSerializer(student_plan,
                                                                         data=request.data.copy(),
                                                                         many=False, partial=True)
        if student_subject_topic_serializer.is_valid():
            student_plan = student_subject_topic_serializer.save(user_pk=request.user.pk)
            student_plan_serializer = StudentSubjectTopicSerializer(student_plan, many=False)
            return Response(student_plan_serializer.data, status=200)
        else:
            return Response({'message': student_subject_topic_serializer.errors}, status=403)


class StudentPlanByPkDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope, )

    def get(self, request, student_plan_pk):
        roles = (TEACHER_ROLE, )
        permission(roles, request.user)

        try:
            student_plan = StudentPlan.objects.get(pk=student_plan_pk)
            student_plan_serializer = StudentSubjectTopicSerializer(student_plan, many=False, context={'is_mid_control': False})
            return Response(student_plan_serializer.data, status=200)
        except StudentPlan.DoesNotExist:
            return Response(status=404)


class OfficeListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        office_list = Office.objects.all().order_by('title')
        office_serializer = OfficeSerializer(office_list, many=True)
        return Response(office_serializer.data, status=200)


class OfficeDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        office_serializer = OfficeSerializer(data=request.data.copy())

        if office_serializer.is_valid():
            office = office_serializer.save(user_pk=request.user.pk)
            office_serializer = OfficeSerializer(office)
            result = {
                'office': office_serializer.data,
                'message': "Successfully added"
            }
            return Response(result, status=201)
        return Response({'message': office_serializer.errors}, status=403)


class ScheduleListView(APIView):
    permission_classes = (TokenHasReadWriteScope, )

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        schedule_list = Schedule.objects.all().order_by('-office', 'week_num', 'start_time', 'finish_time')
        schedule_serializer = ScheduleSerializer(schedule_list, many=True)

        return Response(schedule_serializer.data, status=200)


class AvailableScheduleListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        lesson_group_schedule = LessonGroupSchedule.objects.all()
        schedule_list = Schedule.objects.exclude(schedules__in=lesson_group_schedule).order_by('office', 'week_num', 'start_time', 'finish_time')
        schedule_serializers = ScheduleSerializer(schedule_list, many=True)
        return Response(schedule_serializers.data, status=200)


class LessonGroupDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        errors = {'message': []}

        lesson_group_with_schedule_serializer = LessonGroupWithScheduleSerializers(data=request.data.copy())
        schedules = Schedule.objects.filter(pk__in=request.data['schedules'].copy())

        if lesson_group_with_schedule_serializer.is_valid():
            lesson_group = lesson_group_with_schedule_serializer.save(user_pk=request.user.pk)
            group_schedule = GroupSchedule(lesson_group=lesson_group)
            group_schedule.save(user_pk=request.user.pk)
            for schedule in schedules:
                lesson_group_schedule = LessonGroupSchedule()
                lesson_group_schedule.schedule = schedule
                lesson_group_schedule.group_schedule = group_schedule
                lesson_group_schedule.save(user_pk=request.user.pk)
            data = {
                'group': LessonGroupWithScheduleSerializers(lesson_group).data,
                'message': 'New group has been successfully saved'
            }
            return Response(data, status=201)
        errors['message'].append(lesson_group_with_schedule_serializer.error)
        return Response(errors, status=403)

    def put(self, request, lesson_group_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            lesson_group = LessonGroup.objects.get(pk=lesson_group_pk)
            lesson_group_serializer = LessonGroupWithScheduleSerializers(lesson_group,
                                                                         data=request.data.copy(),
                                                                         partial=True)
            if lesson_group_serializer.is_valid():
                lesson_group_serializer.save(user_pk=request.user.pk)
                schedules_json = request.data['schedules']
                schedules_id = []
                for elem in schedules_json:
                    if isinstance(elem, dict):
                        schedules_id.append(elem['pk'])
                    else:
                        schedules_id.append(elem)

                try:
                    group_schedule = GroupSchedule.objects.get(lesson_group=lesson_group)
                    lesson_group_schedules = LessonGroupSchedule.objects.filter(group_schedule=group_schedule)
                    lesson_group_schedules_id = [ent.schedule.pk for ent in lesson_group_schedules]
                    if set(lesson_group_schedules_id) != set(schedules_id):
                        for ent in lesson_group_schedules:
                            ent.delete(user_pk=request.user.pk)
                        group_schedule.delete(user_pk=request.user.pk)
                        self.set_group_schedule(lesson_group, schedules_id, request.user.pk)
                except GroupSchedule.DoesNotExist:
                    self.set_group_schedule(lesson_group, schedules_id, request.user.pk)

                data = {
                    'group': LessonGroupWithScheduleSerializers(lesson_group).data,
                    'message': 'Группа өзгертілді'
                }
                return Response(data, status=201)

            return Response(lesson_group_serializer.errors, status=400)
        except LessonGroup.DoesNotExist:
            return Response(status=404)

    def delete(self, request, lesson_group_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            lesson_group = LessonGroup.objects.get(pk=lesson_group_pk) # delete
            group_replacement_list = lesson_group.gr_lesson_group.all()
            group_time_transfer_list = lesson_group.lg_group_time_transfer.all()
            delete_ent_list(request.user.pk, group_time_transfer_list)
            delete_ent_list(request.user.pk, group_replacement_list)
            try:
                group_schedule = GroupSchedule.objects.get(lesson_group=lesson_group)
                lesson_group_schedule_list = LessonGroupSchedule.objects.filter(group_schedule=group_schedule)

                delete_ent_list(request.user.pk, lesson_group_schedule_list)
                delete_ent(request.user.pk, group_schedule)
            except GroupSchedule.DoesNotExist:
                pass
            lesson_group_student_list = lesson_group.lesson_group_plan.all()
            for lesson_group_student in lesson_group_student_list:
                lesson_group_student_short_schedule_list = lesson_group_student.short_schedule.all()
                lesson_test_action_list = lesson_group_student.lgs_lesson_test_action.all()
                lesson_video_action_list = lesson_group_student.lgs_lesson_video_action.all()
                student_visit_list = lesson_group_student.lgs_student_visit.all()
                student_group_freeze_list = lesson_group_student.lgs_student_group_freeze.all()

                delete_ent_list(request.user.pk, student_group_freeze_list)
                delete_ent_list(request.user.pk, student_visit_list)
                delete_ent_list(request.user.pk, lesson_video_action_list)
                delete_ent_list(request.user.pk, lesson_test_action_list)
                delete_ent_list(request.user.pk, lesson_group_student_short_schedule_list)
            delete_ent_list(request.user.pk, lesson_group_student_list)
            try:
                material_access_info = lesson_group.lg_material_access_info.get()
                delete_ent(request.user.pk, material_access_info)
            except MaterialAccessInfo.DoesNotExist:
                pass
            group_student_visit_list = lesson_group.lg_group_student_visit.all()
            delete_ent_list(request.user.pk, group_student_visit_list)

            delete_ent(request.user.pk, lesson_group)
            result = {'message': '{} группасы өшірілді'.format(lesson_group.title)}
            return Response(result, status=201) # after all models will delete
        except LessonGroup.DoesNotExist:
            return Response(status=404)

    @staticmethod
    def set_group_schedule(lesson_group, schedules_id, user_pk):
        schedules = Schedule.objects.filter(pk__in=schedules_id)
        group_schedule = GroupSchedule(lesson_group=lesson_group)
        group_schedule.save(user_pk=user_pk)

        for schedule in schedules:
            lesson_group_schedule = LessonGroupSchedule()
            lesson_group_schedule.schedule = schedule
            lesson_group_schedule.group_schedule = group_schedule
            lesson_group_schedule.save(user_pk=user_pk)

# class ChangeScheduleOfLessonGroupView(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def put(self, request):
#         roles = (TEACHER_ROLE,)
#         permission(roles, request.user)
#
#         lesson_group_pk = request.data['pk']
#         schedules = request.data['schedules']
#
#         try:
#             old_lesson_group = LessonGroup.objects.get(pk=lesson_group_pk)
#             old_group_replacement_list = old_lesson_group.gr_lesson_group.all()
#             old_group_time_transfer_list = old_lesson_group.lg_group_time_transfer.all()
#             old_lesson_group_schedule_list = old_lesson_group.groups.all()
#             old_material_access_info_list = old_lesson_group.lg_material_access_info.all()
#
#             old_group_student_visit_list = old_lesson_group.lg_group_student_visit.all()
#             old_lesson_group_student_list = old_lesson_group.lesson_group_plan.all()
#
#             new_lesson_group = LessonGroup(teacher=old_lesson_group.teacher,
#                                            title=old_lesson_group.title,
#                                            student_limit=old_lesson_group.student_limit,
#                                            send_message_on_no_payment=old_lesson_group.send_message_on_no_payment)
#             new_lesson_group.save(user_pk=request.user.pk)
#             for old_ent in old_lesson_group.lesson_group_plan.all():
#                 new_lesson_group_student = LessonGroupStudent(student_plan=old_ent.student_plan,
#                                                               started_date=datetime.date.today(),
#                                                               lesson_group=new_lesson_group)
#                 new_lesson_group_student.save(user_pk=request.user.pk)
#         except LessonGroup.DoesNotExist:
#             return Response(status=404)


class LessonGroupListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        lesson_group_list = LessonGroup.objects.all().order_by('teacher__last_name', 'teacher__first_name', 'title')
        lesson_group_serializers = LessonGroupWithScheduleSerializers(lesson_group_list, many=True)
        return Response(lesson_group_serializers.data, status=200)


class LessonGroupListOffsetView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, start, limit):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        start = int(start)
        limit = int(limit)
        lesson_group_list = LessonGroup.objects.all().order_by('teacher__last_name', 'teacher__first_name', 'title')
        lesson_group_serializers = LessonGroupWithScheduleSerializers(lesson_group_list[start:start+limit], many=True)
        result = {
            'groups': lesson_group_serializers.data,
            'total': lesson_group_list.count()
        }
        return Response(result, status=200)


class LessonGroupStudentDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        lesson_group_student_serializer = LessonGroupStudentSerializer(data=request.data.copy(), many=False)
        errors = {'error': []}
        if not lesson_group_student_serializer.is_valid():
            errors['error'].append(lesson_group_student_serializer.errors)
        else:
            lesson_group_student = lesson_group_student_serializer.save(user_pk=request.user.pk)
            lesson_group_student_short_schedule_serializer = LessonGroupStudentShortScheduleSerializer(
                data=request.data['lesson_group_student_short_schedule'],
                many=True)
            if lesson_group_student_short_schedule_serializer.is_valid():
                lesson_group_student_short_schedule = lesson_group_student_short_schedule_serializer\
                    .save(user_pk=request.user.pk, lesson_group_student=lesson_group_student)
            lesson_group_student = LessonGroupStudent.objects.get(pk=lesson_group_student.pk)
            result = {
                'group_student_plan': LessonGroupStudentSerializer(lesson_group_student, many=False).data,
                'message': "Student's plan added to group"
            }
            return Response(result, status=201)
        errors = {'message': []}
        errors['message'].append(lesson_group_student_serializer.error)
        return Response(errors, status=403)

    def put(self, request, lesson_group_student_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            lesson_group_student = LessonGroupStudent.objects.get(pk=lesson_group_student_pk)
            lesson_group_student_serializer = LessonGroupStudentSerializer(lesson_group_student,
                                                                           data=request.data.copy(),
                                                                           partial=True,
                                                                           many=False)
            if lesson_group_student_serializer.is_valid():
                lesson_group_student = lesson_group_student_serializer.save(user_pk=request.user.pk)
                student_short_schedule = []
                student_short_schedule_new = []
                for item in request.data['lesson_group_student_short_schedule']:
                    if item['pk'] is None:
                        student_short_schedule_new.append(item)
                    else:
                        student_short_schedule.append(item['pk'])
                student_short_schedule_ent = LessonGroupStudentShortSchedule.objects.filter(
                    lesson_group_student=lesson_group_student
                )

                if student_short_schedule_ent.count() > len(student_short_schedule):
                    student_short_schedule_ent_excludes = student_short_schedule_ent.exclude(
                        pk__in=student_short_schedule
                    )
                    for ent in student_short_schedule_ent_excludes:
                        ent.delete(user_pk=request.user.pk)
                elif len(student_short_schedule_new) > 0:
                    lesson_group_student_short_schedule_serializer = LessonGroupStudentShortScheduleSerializer(
                        data=student_short_schedule_new,
                        many=True)
                    if lesson_group_student_short_schedule_serializer.is_valid():
                        lesson_group_student_short_schedule = lesson_group_student_short_schedule_serializer \
                            .save(user_pk=request.user.pk, lesson_group_student=lesson_group_student)
                lesson_group_student = LessonGroupStudent.objects.get(pk=lesson_group_student.pk)
                result = {
                    'group_student_plan': LessonGroupStudentSerializer(lesson_group_student, many=False).data,
                    'message': "Student's plan successfully edited"
                }
                return Response(result, status=201)
            else:
                return Response({'error': lesson_group_student_serializer.errors}, status=400)
        except LessonGroupStudent.DoesNotExist:
            return Response(status=404)

    def delete(self, request, group_student_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            group_student = LessonGroupStudent.objects.get(pk=group_student_pk)

            lesson_group_student_short_schedule_list = group_student.short_schedule.all()
            lesson_test_action_list = group_student.lgs_lesson_test_action.all()
            lesson_video_action_list = group_student.lgs_lesson_video_action.all()
            student_visit_list = group_student.lgs_student_visit.all()
            student_group_freeze_list = group_student.lgs_student_group_freeze.all()

            delete_ent_list(request.user.pk, student_group_freeze_list)
            delete_ent_list(request.user.pk, student_visit_list)
            delete_ent_list(request.user.pk, lesson_video_action_list)
            delete_ent_list(request.user.pk, lesson_test_action_list)
            delete_ent_list(request.user.pk, lesson_group_student_short_schedule_list)

            group_student.delete(user_pk=request.user.pk)
            result = {
                'message': "Student's plan successfully deleted from group"
            }
            return Response(result, status=201)
        except LessonGroupStudent.DoesNotExist:
            return Response(status=404)


class LessonGroupStudentListView(APIView):
    permission_classes = (TokenHasReadWriteScope, )

    def get(self, request, lesson_group_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        lesson_group_students = LessonGroupStudent.objects.filter(lesson_group__pk=lesson_group_pk)\
            .order_by('student_plan__student__last_name', 'student_plan__student__first_name')
        lesson_group_student_serializers = LessonGroupStudentSerializer(lesson_group_students, many=True)
        return Response(lesson_group_student_serializers.data, status=200)


class LessonGroupListByTeacherView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        lesson_group_list = LessonGroup.objects.filter(Q(teacher=request.user)).order_by('title')
        group_replacement = GroupReplacement.objects.filter(Q(teacher__user=request.user)
                                                            & Q(date=datetime.date.today()))
        lesson_groups = []
        for lesson_group in lesson_group_list:
            lesson_groups.append(lesson_group)
        for ent in group_replacement:
            lesson_groups.append(ent.lesson_group)
        lesson_group_serializers = LessonGroupFullSerializer(lesson_groups, many=True)
        return Response(lesson_group_serializers.data, status=200)


class GroupReplaceListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, group_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        group_replacement_list = GroupReplacement.objects.filter(lesson_group__pk=group_pk).order_by('-date')
        group_replacement_list_serializer = GroupReplacementSerializer(group_replacement_list, many=True)
        return Response(group_replacement_list_serializer.data, status=200)


class GroupReplacementDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        group_replacement_serializer = GroupReplacementSerializer(data=request.data.copy(), many=True)
        if group_replacement_serializer.is_valid():
            group_replacements = group_replacement_serializer.save(user_pk=request.user.pk)
            group_replacement_serializers = GroupReplacementSerializer(group_replacements, many=True)
            data = {
                'group_replacement': group_replacement_serializers.data,
                'message': 'Successfully saved'
            }
            return Response(data, status=201)
        else:
            return Response(group_replacement_serializer.errors, status=400)

    def put(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        try:
            group_replacement = GroupReplacement.objects.get(pk=request.data['pk'])
            group_replacement_serializer = GroupReplacementSerializer(group_replacement, data=request.data.copy(), many=False, partial=True)
            if group_replacement_serializer.is_valid():
                group_replacement = group_replacement_serializer.save(user_pk=request.user.pk)
                group_replacement_serializer = GroupReplacementSerializer(group_replacement)
                data = {
                    'group_replacement': group_replacement_serializer.data,
                    'message': "Replacement or Cancellaction successfully changed"
                }
                return Response(data, status=201)
            else:
                return Response(group_replacement_serializer.errors, status=400)
        except GroupReplacement.DoesNotExist:
            return Response(status=404)

    def delete(self, request, group_replacement_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            group_replacement = GroupReplacement.objects.get(pk=group_replacement_pk)
            group_replacement.delete(user_pk=request.user.pk)
            message = {
                'message': 'Group replacement or cancellation successfully deleted'
            }
            return Response(message, status=201)
        except GroupReplacement.DoesNotExist:
            return Response(status=404)


class DayOffListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        day_off_list = DayOff.objects.all().order_by('-date')
        day_off_list_serializer = DayOffSerializer(day_off_list, many=True)

        return Response(day_off_list_serializer.data, status=200)


class DayOffDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        day_off_list_serializer = DayOffSerializer(data=request.data.copy(), many=True)
        if day_off_list_serializer.is_valid():
            day_off_list_serializer.save(user_pk=request.user.pk)
            result = {
                'day_off_list': day_off_list_serializer.data,
                'message': "day off successfully added"
            }
            return Response(result, status=201)
        return Response(day_off_list_serializer.errors, status=400)

    def put(self, request, day_off):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        try:
            day_off_ent = DayOff.objects.get(pk=day_off)
            day_off_serializer = DayOffSerializer(day_off_ent, data=request.data.copy(), many=False, partial=True)
            if day_off_serializer.is_valid():
                day_off_serializer.save(user_pk=request.user.pk)
                result = {
                    'day_off': day_off_serializer.data,
                    'message': 'day off successfully edited'
                }
                return Response(result, status=201)
            return Response(day_off_serializer.errors, status=400)
        except DayOff.DoesNotExist:
            return Response(status=404)

    def delete(self, request, day_off):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        try:
            day_off_ent = DayOff.objects.get(pk=day_off)
            day_off_ent.delete(user_pk=request.user.pk)
            result = {
                'message': "Day off successfully deleted"
            }
            return Response(result, status=200)
        except DayOff.DoesNotExist:
            return Response(status=404)


class GroupTimeTransferListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, lesson_group_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        group_time_transfer = GroupTimeTransfer.objects.filter(lesson_group__pk=lesson_group_pk)
        group_time_transfer_serializer = GroupTimeTransferSerializer(group_time_transfer, many=True)
        return Response(group_time_transfer_serializer.data, status=200)


class GroupTimeTransferDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        group_time_transfer_serializer = GroupTimeTransferSerializer(data=request.data.copy(), many=False)
        if group_time_transfer_serializer.is_valid():
            group_time_transfer_serializer.save(user_pk=request.user.pk)
            result = {
                'group_time_transfer': group_time_transfer_serializer.data,
                'message': 'Group time transfer successfully saved'
            }
            return Response(result, status=201)
        return Response(group_time_transfer_serializer.errors, status=400)

    def delete(self, request, group_time_transfer_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            group_time_transfer = GroupTimeTransfer.objects.get(pk=group_time_transfer_pk)
            group_time_transfer.delete(user_pk=request.user.pk)
            result = {
                'message': "Group time transfer successfully deleted"
            }
            return Response(result, status=201)
        except GroupTimeTransfer.DoesNotExist:
            return Response(status=404)


class UpdateGroupListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        lesson_groups = LessonGroup.objects.all().exclude(pk__in=request.data.copy())
        lesson_groups_serializer = LessonGroupWithScheduleSerializers(lesson_groups, many=True)
        return Response(lesson_groups_serializer.data, status=200)


class ResetMaterialAccessView(APIView):

    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)
        lesson_groups = LessonGroup.objects.filter(teacher=request.user)
        for lesson_group in lesson_groups:
            set_ip(lesson_group, request.META, request.user.pk)
        return Response(status=200)


# from ..models import SubjectPlan, TopicPlan
# from materials.models import Topic
#
# class DeleteIncorrectTopicPlanView(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#
#         quizes = Topic.objects.filter(is_mid_control=True)
#
#         for quiz in quizes:
#             subject_plans = SubjectPlan.objects.all()
#             for subject_plan in subject_plans:
#                 try:
#                     topic_plan = subject_plan.topic_plan.get(topic=quiz)
#                     topic_plan.delete(user_pk=request.user.pk)
#                 except TopicPlan.DoesNotExist:
#                     pass
#         return Response(status=201)
#
# class SetUnsettedTopicPlanView(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#
#         quizes = Topic.objects.filter(is_mid_control=True)
#
#         for quiz in quizes:
#             if quiz.subject is None:
#                 subject = quiz.parent.subject
#             else:
#                 subject = quiz.subject
#             subject_plans = SubjectPlan.objects.filter(subject=subject)
#             for subject_plan in subject_plans:
#                 try:
#                     subject_plan.topic_plan.get(topic=quiz)
#                 except TopicPlan.DoesNotExist:
#                     topic_plan = TopicPlan()
#                     topic_plan.subject_plan = subject_plan
#                     topic_plan.topic = quiz
#                     topic_plan.save(user_pk=1)
#         return Response(status=201)



# class SetStudentsShortSchedules(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#
#         lesson_groups = LessonGroup.objects.all()
#         for lesson_group in lesson_groups:
#             students = lesson_group.lesson_group_plan.all()
#             group_schedules = lesson_group.groups.all()
#             for student in students:
#                 for group_schedule in group_schedules:
#                     week_num = group_schedule.schedule.week_num
#                     week_day_sign = None
#                     if week_num in [1, 2]:
#                         week_day_sign = 1
#                     elif week_num in [3, 4]:
#                         week_day_sign = 2
#                     elif week_num in [5, 6]:
#                         week_day_sign = 3
#                     try:
#                         lesson_group_student_short_schedule = LessonGroupStudentShortSchedule.objects.get(
#                             lesson_group_student=student,
#                             week_day_sign=week_day_sign
#                         )
#                         student_user = lesson_group_student_short_schedule.lesson_group_student.student_plan.student
#                         print('exists', lesson_group_student_short_schedule, student_user.last_name, student_user.first_name)
#                     except LessonGroupStudentShortSchedule.DoesNotExist:
#                         lesson_group_student_short_schedule = LessonGroupStudentShortSchedule()
#                         lesson_group_student_short_schedule.lesson_group_student = student
#                         lesson_group_student_short_schedule.week_day_sign = week_day_sign
#                         lesson_group_student_short_schedule.save()
#         return Response(status=201)



# from django.conf import settings
# from portal.api.constants import TEACHER_DEFAULT_PASSWORD, TEACHER_ROLE
# import json
# from django.db.models import Q
# from lessonProgress.models import GroupStudentVisit, StudentVisit
# import datetime
# import io
# class MigrateStudentProgress(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#         user_pk = request.user.pk
#         # path = settings.BASE_DIR + '\material_json\\all_students_progress.txt'
#         path = '/home/zhambyl/portal/backend/portal.django/src/material_json/all_students_progress.txt'
#         f = open(path, 'r')
#         data_json = json.loads(f.read())
#         f.close()
#
#         student_plan_does_not_exists = ""
#         lesson_group_does_not_exists = ""
#
#         for item in data_json:
#             try:
#                 group_name = item['group_name']
#                 group_name = group_name.replace(' (м)', '')
#                 group_name = group_name.replace(' (М)', '')
#                 if group_name[3:4] == 'с':
#                     group_name = group_name[:3] + group_name[4:]
#                 group_name = group_name.strip()
#                 student_plan = StudentPlan.objects.get(Q(student__last_name=item['surname'])
#                                                        & Q(student__first_name=item['name'])
#                                                        & Q(subject__title=item['subject_name']))
#                 lesson_group = LessonGroup.objects.get(title=group_name)
#
#                 started_date = datetime.datetime.strptime(item['created_date'], '%Y-%m-%d').date()
#
#                 lesson_group_student = self.get_lesson_group_student(student_plan, lesson_group, started_date, request.user.pk)
#                 abs_date = datetime.datetime.strptime(item['abs_date'], '%Y-%m-%d').date()
#                 group_student_visit = self.get_group_student_visit_ent(lesson_group, abs_date, request.user.pk)
#
#                 attendance = True if item['attendance'] == '1' else False
#                 home_work = 0.0 if float(item['home_work']) == -0.1 else float(item['home_work'])
#                 no_home_work = True if float(item['home_work']) == -0.1 else False
#
#                 try:
#                     student_visit = StudentVisit.objects.get(group_student_visit=group_student_visit,
#                                                              lesson_group_student=lesson_group_student)
#                 except:
#                     student_visit = StudentVisit()
#                     student_visit.group_student_visit = group_student_visit
#                     student_visit.lesson_group_student = lesson_group_student
#                     student_visit.attendance = attendance
#                     student_visit.home_work = home_work
#                     student_visit.no_home_work = no_home_work
#                     student_visit.save(user_pk=request.user.pk)
#
#             except StudentPlan.DoesNotExist:
#                 # student_plan_does_not_exists += item['surname'] + ' ' + item['name'] + ' -> ' + item['group_name'] + ': ' + item['subject_name'] + '\n'
#                 pass
#             except LessonGroup.DoesNotExist:
#                 # lesson_group_does_not_exists += item['group_name'] + '\n'
#                 pass
#         # if student_plan_does_not_exists:
#         #     # f = open('student_does_not_find.txt', 'w')
#         #     f = io.open('student_does_not_find.txt', 'w', encoding='utf8')
#         #     f.write(student_plan_does_not_exists)
#         #     f.close()
#         # if lesson_group_does_not_exists:
#         #     # f = open('lesson_group_does_not_find.txt', 'w')
#         #     f = io.open('lesson_group_does_not_find.txt', 'w', encoding='utf8')
#         #     f.write(lesson_group_does_not_exists)
#         #     f.close()
#         return Response(status=201)
#
#
#     def get_group_student_visit_ent(self, lesson_group, abs_date, user_pk):
#         try:
#             return GroupStudentVisit.objects.get(Q(lesson_group=lesson_group)
#                                                  & Q(abs_date=abs_date))
#         except GroupStudentVisit.DoesNotExist:
#             group_student_visit = GroupStudentVisit()
#             group_student_visit.lesson_group = lesson_group
#             group_student_visit.abs_date = abs_date
#             group_student_visit.save(user_pk=user_pk)
#             return group_student_visit
#
#     def get_lesson_group_student(self, student_plan, lesson_group, started_date, user_pk):
#         try:
#             return LessonGroupStudent.objects.get(Q(student_plan=student_plan)
#                                                   & Q(lesson_group=lesson_group))
#         except LessonGroupStudent.DoesNotExist:
#             lesson_group_student = LessonGroupStudent()
#             lesson_group_student.student_plan = student_plan
#             lesson_group_student.lesson_group = lesson_group
#             lesson_group_student.started_date = started_date
#             lesson_group_student.save(user_pk=user_pk)
#             return lesson_group_student

# class SetDefaultSchedules(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = DEVELOPER_ROLE
#         permission(roles, request.user)
#
#         office_list = Office.objects.all()
#
#         times = [
#             {
#                 'start_time': '15:00:00',
#                 'finish_time': '16:30:00',
#             },
#             {
#                 'start_time': '16:40:00',
#                 'finish_time': '18:10:00',
#             },
#             {
#                 'start_time': '18:30:00',
#                 'finish_time': '20:00:00',
#             }
#         ]
#         week_days = dict(WEEK_DAY_CHOICES)
#         week_days.pop(7, None)
#         for office in office_list:
#             for week_key in week_days:
#                 for time in times:
#                     schedule = Schedule()
#                     schedule.office = office
#                     schedule.week_num = week_key
#                     schedule.start_time = time['start_time']
#                     schedule.finish_time = time['finish_time']
#                     schedule.save(user_pk=request.user.pk)
#
#         return Response(status=201)