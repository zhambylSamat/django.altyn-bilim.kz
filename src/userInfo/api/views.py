from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from portal.api.utils import permission
from django.db.models import Q
import datetime

from portal.api.constants import (
    DEVELOPER_ROLE,
    ADMIN_ROLE,
    SUPER_MODERATOR_ROLE,
    MODERATOR_ROLE,
    STUDENT_ROLE,
    TEACHER_ROLE,
    PARENT_ROLE,
    FULL_STAFF_ROLES,

    STUDENT_DEFAULT_PASSWORD,
    TEACHER_DEFAULT_PASSWORD,
    STAFF_DEFAULT_PASSWORD,
)
from .serializers import (
    UserStudentSerializer,
    StudentSerializer,
    ParentSerializer,
    UserStaffSerializer,
    StaffSerializer,
    StudentFreezeSerializer,
    StudentGroupFreezeSerializer,
)
from portal.api.serializer import UserSerializer
from ..models import UserRole, Student, Parent, Staff, StudentFreeze, StudentGroupFreeze
from portal.api.utils import (
    generate_random_username,
    user_does_not_exists,
    revoke_token,
    increase_one_day_in_date
)
from .utils import student_verification, staff_verification, access_to_edit_profile, access_to_create_profile


class StudentDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = [DEVELOPER_ROLE, ADMIN_ROLE, SUPER_MODERATOR_ROLE, MODERATOR_ROLE]
        permission(roles, request.user)
        error_messages = {'message': []}
        verification = student_verification(request.data)
        if verification:
            return verification
        student_user_serializer = UserSerializer(data=request.data['user'].copy())
        student_serializer = StudentSerializer(data=request.data['student'].copy())
        student_user = None
        if student_user_serializer.is_valid() and student_serializer.is_valid():
            student_user = student_user_serializer.save(is_active=True, password=STUDENT_DEFAULT_PASSWORD)
            student_user.set_password(STUDENT_DEFAULT_PASSWORD)
            student_user.save()
            UserRole(user=student_user, role=STUDENT_ROLE).save()
            student = student_serializer.save(user=student_user, user_pk=request.user.pk)
            for item in request.data['student']['parents']:
                parent_error_messages = self.parent_save(item, request.user.pk, student)
                if parent_error_messages:
                    error_messages['message'].append(parent_error_messages)

        if error_messages['message']:
            return Response(error_messages, status=400)
        student_serializer = UserStudentSerializer(student_user, many=False)
        return Response(student_serializer.data, status=200)

    def put(self, request, user_pk):
        roles = [DEVELOPER_ROLE, ADMIN_ROLE, SUPER_MODERATOR_ROLE, MODERATOR_ROLE]
        permission(roles, request.user)

        verification = student_verification(request.data)
        if verification:
            return verification
        student_pk = request.data['student']['pk']
        error_messages = {"message": []}

        try:
            student_user = User.objects.get(pk=user_pk)
            student = Student.objects.get(pk=student_pk)
        except (User.DoesNotExist, Student.DoesNotExist):
            return user_does_not_exists()

        student_user_serializer = UserSerializer(student_user, data=request.data['user'].copy(), many=False, partial=True)
        student_serializer = StudentSerializer(student, data=request.data['student'].copy(), many=False, partial=True)
        if student_user_serializer.is_valid() and student_serializer.is_valid():
            student_user_serializer.save()
            student_serializer.save(user_pk=request.user.pk)
        else:
            error_messages['message'].append(student_user_serializer.errors)
            error_messages['message'].append(student_serializer.errors)

        # self.remove_parents(request.data['student']['parents'], request.data['student']['pk'], request.user.pk)
        for parent_request in request.data['student']['parents']:
            parent_error_messages = self.parent_save(parent_request, request.user.pk, student)
            if parent_error_messages:
                error_messages['message'].append(parent_error_messages)

        if error_messages['message']:
            return Response(error_messages, status=206)
        else:
            student_serializer = UserStudentSerializer(student_user, many=False)
            return Response(student_serializer.data, status=200)


    def parent_save(self, parent_json, user_pk, student=None):
        error_messages = []
        if parent_json['user']['pk'] and parent_json['parent']['pk']:
            try:
                parent_user = User.objects.get(pk=parent_json['user']['pk'])
                parent = Parent.objects.get(pk=parent_json['parent']['pk'])
            except (User.DoesNotExist, Student.DoesNotExist):
                user_does_not_exists()
            parent_user_serializer = UserSerializer(parent_user, data=parent_json['user'].copy(), many=False,
                                                    partial=True)
            parent_serializer = ParentSerializer(parent, data=parent_json['parent'].copy(), many=False, partial=True)

            if parent_user_serializer.is_valid() and parent_serializer.is_valid():
                parent_user_serializer.save()
                parent_serializer.save(user_pk=user_pk)
            else:
                error_messages.append(parent_user_serializer.errors)
                error_messages.append(parent_serializer.errors)
        elif parent_json['user']['first_name'] and parent_json['user']['last_name']:
            parent_user_serializer = UserSerializer(data=parent_json['user'].copy())
            parent_serializer = ParentSerializer(data=parent_json['parent'].copy())

            if parent_user_serializer.is_valid() and parent_serializer.is_valid():
                parent_user = parent_user_serializer.save(is_active=True, username=generate_random_username())
                UserRole(user=parent_user, role=PARENT_ROLE).save()
                parent_serializer.save(user=parent_user, student=student, user_pk=user_pk)
            else:
                error_messages.append(parent_user_serializer.errors)
                error_messages.append(parent_serializer.errors)
        return error_messages

    # def remove_parents(self, parent_json, student_pk, user_pk):
    #     print(parent_json, student_pk)
    #     parent_ids = [parent['parent']['pk'] for parent in parent_json]
    #
    #     parents = Parent.objects.filter(student_pk=student_pk)
    #     for parent in parents:
    #         if parent.pk not in parent_ids:
    #             user_id = parent.user.pk
    #             parent.delete(user_pk=user_pk)
    #             User.objects.get(pk=user_id).delete


class ListStudentView(APIView):
    permission_classes = (TokenHasReadWriteScope,)
    # permission_classes = (AllowAny,)

    def get(self, request):
        roles = [DEVELOPER_ROLE, ADMIN_ROLE, SUPER_MODERATOR_ROLE, MODERATOR_ROLE]
        permission(roles, request.user)
        students = User.objects.filter(user_role__role=STUDENT_ROLE)
        student_serializer = UserStudentSerializer(students, many=True)
        return Response(student_serializer.data, status=200)


class StudentListOffsetView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, start, limit):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        start = int(start)
        limit = int(limit)
        students = User.objects.filter(user_role__role=STUDENT_ROLE).order_by('last_name', 'first_name')
        student_serializer = UserStudentSerializer(students[start:start+limit], many=True)
        result = {
            'students': student_serializer.data,
            'total': students.count()
        }
        return Response(result, status=200)


class ResetStudentPasswordView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, user_pk):

        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            user_does_not_exists()

        try:
            student = user.user_student.get()
        except Exception:
            user_does_not_exists()

        student.is_password_reset = True
        student.save(user_pk=request.user.pk)
        user.set_password(STUDENT_DEFAULT_PASSWORD)
        user.save()
        revoke_token(user.username)
        data = {
            'message': 'Password of ' + user.get_full_name() + ' successfully reset',
            'is_password_reset': student.is_password_reset
        }
        return Response(data, status=201)


class StudentPaymentView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, user_pk, has_payment):
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            user_does_not_exists()

        try:
            student = user.user_student.get()
        except Exception:
            user_does_not_exists()

        message = ''
        if has_payment == "YES":
            student.has_payment = True
            if student.has_contract:
                student.force_access_until = None
                user.save()
            student.save(user_pk=request.user.pk)
            message = 'Payment access status successfully set to ' + user.get_full_name()
        elif has_payment == "NO":
            student.has_payment = False
            student.force_access_until = None
            student.save(user_pk=request.user.pk)
            user.save()
            revoke_token(user.username)
            message = 'No Payment status successfully set to ' + user.get_full_name()
        else:
            data = {'message': 'error'};
            return Response(data, status=400)
        data = {
            'has_payment': student.has_payment,
            'message': message
        }
        return Response(data, status=201)


class StudentContractView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, user_pk, has_contract):
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            user_does_not_exists()

        try:
            student = user.user_student.get()
        except Exception:
            user_does_not_exists()

        message = ''
        if has_contract == "YES":
            student.has_contract = True
            if student.has_payment:
                student.force_access_until = None
                user.save()
            student.save(user_pk=request.user.pk)
            message = "Contract access status successfully set to " + user.get_full_name()
        elif has_contract == "NO":
            student.has_contract = False
            student.force_access_until = None
            student.save(user_pk=request.user.pk)
            user.save()
            revoke_token(user.username)
            message = "No Contract status successfully set to " + user.get_full_name()
        else:
            data = {'message': 'error'}
            return Response(data, status=400)
        data = {
            'message': message,
            'has_contract': student.has_contract
        }
        return Response(data, status=201)


class ListTeacherView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        staffs = User.objects.filter(user_role__role=TEACHER_ROLE)
        staff_serializer = UserStaffSerializer(staffs, many=True)
        return Response(staff_serializer.data, status=200)


class StaffDetailView(APIView):

    permission_classes = (TokenHasReadWriteScope, )

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        error_messages = {'message': []}
        verification = staff_verification(request.data)
        if verification:
            return verification
        access = access_to_create_profile(request.user, request.data['user']['role'])
        if access:
            return access

        staff_user_serializer = UserSerializer(data=request.data['user'].copy())
        staff_serializer = StaffSerializer(data=request.data['staff'].copy())
        role = request.data['user']['role']
        default_password = TEACHER_DEFAULT_PASSWORD if role == TEACHER_ROLE else STAFF_DEFAULT_PASSWORD
        staff_user = None
        if staff_user_serializer.is_valid():
            if staff_serializer.is_valid():
                staff_user = staff_user_serializer.save(is_active=True)
                staff_user.set_password(default_password)
                staff_user.save()
                UserRole(user=staff_user, role=role).save(user_pk=request.user.pk)
                staff_serializer.save(user=staff_user, user_pk=request.user.pk)
            else:
                error_messages['message'].append(staff_serializer.errors)
        else:
            error_messages['message'].append(staff_user_serializer.errors)

        if error_messages['message']:
            return Response(error_messages, status=400)
        staff_serializer = UserStaffSerializer(staff_user, many=False)
        return Response(staff_serializer.data, status=200)

    def put(self, request, user_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        verification = staff_verification(request.data)
        if verification:
            return verification
        access = access_to_edit_profile(user_pk, request.user, request.data['user']['role'])
        if access:
            return access

        staff_pk = request.data['staff']['pk']
        error_messages = {"message": []}

        try:
            staff_user = User.objects.get(pk=user_pk)
            staff = Staff.objects.get(pk=staff_pk)
        except (User.DoesNotExist, Staff.DoesNotExist):
            return user_does_not_exists()

        staff_user_serializer = UserSerializer(staff_user, data=request.data['user'], many=False, partial=True)
        staff_serializer = StaffSerializer(staff, data=request.data['staff'].copy(), many=False, partial=True)
        role = request.data['user']['role']

        if staff_user_serializer.is_valid():
            if staff_serializer.is_valid():
                staff_user_serializer.save()
                if staff_user.user_role.get().role != role:
                    user_role = UserRole.objects.get(user=staff_user)
                    user_role.role = role
                    user_role.save(user_pk=request.user.pk)
                staff_serializer.save(user_pk=request.user.pk)
            else:
                error_messages['message'].append(staff_serializer.errors)
        else:
            error_messages['message'].append(staff_user_serializer.errors)

        if error_messages['message']:
            return Response(error_messages, status=206)
        else:
            staff_serializer = UserStaffSerializer(staff_user, many=False)
            return Response(staff_serializer.data, status=200)


class ListStaffView(APIView):
    permission_classes = (TokenHasReadWriteScope,)
    # permission_classes = (AllowAny,)

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        staffs = User.objects.filter(user_role__role__in=FULL_STAFF_ROLES)
        staff_serializer = UserStaffSerializer(staffs, many=True)
        return Response(staff_serializer.data, status=200)


class ResetStaffPasswordView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, user_pk):

        access = access_to_edit_profile(user_pk, request.user)
        if access:
            return access

        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            user_does_not_exists()

        try:
            staff = user.user_staff.get()
        except Exception:
            user_does_not_exists()

        default_password = TEACHER_DEFAULT_PASSWORD \
                            if user.user_role.get().role == TEACHER_ROLE \
                            else STAFF_DEFAULT_PASSWORD

        staff.is_password_reset = True
        staff.save(user_pk=request.user.pk)
        user.set_password(default_password)
        user.save()
        revoke_token(user.username)
        data = {
            'message': 'Password of ' + user.get_full_name() + ' successfully reset',
            'is_password_reset': staff.is_password_reset
        }
        return Response(data, status=201)


class UpdateStudentListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        students = User.objects.filter(user_role__role=STUDENT_ROLE).exclude(pk__in=request.data.copy())
        student_serializer = UserStudentSerializer(students, many=True)
        return Response(student_serializer.data, status=200)


class StudentFreezeDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, user_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        student_freeze = StudentFreeze.objects.filter(student__pk=user_pk)
        student_freeze_serializer = StudentFreezeSerializer(student_freeze, many=True)
        return Response(student_freeze_serializer.data, status=200)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        student_freeze_serializer = StudentFreezeSerializer(data=request.data.copy())
        if student_freeze_serializer.is_valid():
            from_date = student_freeze_serializer.validated_data['from_date']
            to_date = student_freeze_serializer.validated_data['to_date']
            student = student_freeze_serializer.validated_data['student']
            has_abs = self.get_has_abs_by_user(student, from_date, to_date)
            if not has_abs:
                student_freeze_serializer.save(user_pk=request.user.pk)
                result = {
                    'student_freeze': student_freeze_serializer.data,
                    'message': 'Оқушының замарозкасы енгізілді'
                }
                return Response(result, status=201)
            result = {
                'message': 'Оқушының замарозкасы енгізілмеді. Мұғалім баға қойып тастады'
            }
            return Response(result, status=400)

        return Response(student_freeze_serializer.errors, status=400)

    def put(self, request, student_freeze_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            student_freeze = StudentFreeze.objects.get(pk=student_freeze_pk)
            student_freeze_serializer = StudentFreezeSerializer(student_freeze, data=request.data.copy(), partial=True)
            if student_freeze_serializer.is_valid():
                from_date = student_freeze_serializer.validated_data['from_date']
                to_date = student_freeze_serializer.validated_data['to_date']
                if from_date == student_freeze.from_date:
                    if to_date > datetime.date.today():
                        student_freeze_serializer.save(user_pk=request.user.pk)
                        result = {
                            'student_freeze': student_freeze_serializer.data,
                            'message': 'Оқушының замарозкасы өзгертілді',
                        }
                        return Response(result, status=201)
                    elif to_date <= datetime.date.today():
                        if increase_one_day_in_date(to_date) == datetime.date.today():
                            has_abs = self.get_has_abs(student_freeze, datetime.date.today(), datetime.date.today())
                        else:
                            has_abs = self.get_has_abs(student_freeze, to_date, datetime.date.today())
                        if not has_abs:
                            student_freeze_serializer.save(user_pk=request.user.pk)
                            result = {
                                'student_freeze': student_freeze_serializer.data,
                                'message': 'Оқушының замарозкасы өзгертілді',
                            }
                            return Response(result, status=201)
                        result = {
                            'message': 'Оқушының замарозкасын өзгертуге болмайды. Мұғалім баға қойып тастады'
                        }
                        return Response(result, status=400)
                else:
                    has_abs = self.get_has_abs(student_freeze, to_date, datetime.date.today())
                    if not has_abs:
                        student_freeze_serializer.save(user_pk=request.user.pk)
                        result = {
                            'student_freeze': student_freeze_serializer.data,
                            'message': 'Оқушының замарозкасы өзгертілді',
                        }
                        return Response(result, status=201)
                    result = {
                        'message': 'Оқушының замарозкасын өзгертуге болмайды. Мұғалім баға қойып тастады'
                    }
                    return Response(result, status=400)

            return Response(student_freeze_serializer.errors, status=400)
        except StudentFreeze.DoesNotExist:
            return Response(status=404)

    def delete(self, request, student_freeze_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            student_freeze = StudentFreeze.objects.get(pk=student_freeze_pk)
            has_abs = self.get_has_abs(student_freeze, student_freeze.from_date, datetime.date.today())
            if not has_abs:
                student_freeze.delete(user_pk=request.user.pk)
                result = {
                    'message': 'Оқушының замарозкасы өшірілді'
                }
                return Response(result, status=201)
            result = {
                'message': 'Оқушының замарозкасын өшіруге болмайды. Мұғалім баға қойып тастады'
            }
            return Response(result, status=400)
        except StudentFreeze.DoesNotExist:
            return Response(status=404)

    @staticmethod
    def get_has_abs(student_freeze, from_date, to_date):
        student_plan_list = student_freeze.student.s_student_plan.all()
        for student_plan in student_plan_list:
            lesson_group_student_list = student_plan.sp_lesson_group_student.all()
            for lesson_group_student in lesson_group_student_list:
                group_student_visit_count = lesson_group_student.lesson_group.lg_group_student_visit.filter(
                    Q(abs_date__gte=from_date)
                    & Q(abs_date__lte=to_date))
                if group_student_visit_count.count() > 0:
                    return True
        return False

    @staticmethod
    def get_has_abs_by_user(user, from_date, to_date):
        student_plan_list = user.s_student_plan.all()
        for student_plan in student_plan_list:
            lesson_group_student_list = student_plan.sp_lesson_group_student.all()
            for lesson_group_student in lesson_group_student_list:
                group_student_visit_count = lesson_group_student.lesson_group.lg_group_student_visit.filter(
                    Q(abs_date__gte=from_date)
                    & Q(abs_date__lte=to_date)).count()
                if group_student_visit_count > 0:
                    return True
        return False


class StudentGroupFreezeListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, lesson_group_student_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        student_group_freeze_list = StudentGroupFreeze.objects.filter(lesson_group_student__pk=lesson_group_student_pk)
        student_group_freeze_serializers = StudentGroupFreezeSerializer(student_group_freeze_list, many=True)
        return Response(student_group_freeze_serializers.data, status=200)


class StudentGroupFreezeDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        student_group_freeze_serializer = StudentGroupFreezeSerializer(data=request.data.copy(), partial=True)
        if student_group_freeze_serializer.is_valid():
            if self.get_has_no_abs(student_group_freeze_serializer.validated_data['lesson_group_student']):
                student_group_freeze_serializer.save(user_pk=request.user.pk)
                result = {
                    'message': 'Оқушының группаға байланысты замарозкасы енгізілді',
                    'student_group_freeze': student_group_freeze_serializer.data
                }
                return Response(result, status=201)
            result = {
                'message': 'Оқушының группаға байланысты заморозкасы енгізілмеді. Мұғалім баға қойып қойды'
            }
            return Response(result, status=400)
        return Response(student_group_freeze_serializer.errors, status=400)

    def delete(self, request, student_group_freeze_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        try:
            student_group_freeze = StudentGroupFreeze.objects.get(pk=student_group_freeze_pk)
            if self.get_has_no_abs(student_group_freeze.lesson_group_student):
                student_group_freeze.delete(user_pk=request.user.pk)
                result = {
                    'message': 'Оқушының группаға байланысты замарозкасы өшірілді',
                }
                return Response(result, status=201)
            result = {
                'message': 'Оқушының группаға байлынсыты замарозкасы ошірілмеді. Мұғалім баға қойып қойды'
            }
            return Response(result, status=400)
        except StudentGroupFreeze.DoesNotExist:
            return Response(status=404)

    @staticmethod
    def get_has_no_abs(lesson_group_student):
        group_student_visit = lesson_group_student.lesson_group.lg_group_student_visit.filter(
            abs_date=datetime.date.today())
        return group_student_visit.count() == 0


# class SwapFirstAndLastNameFromStudent(APIView):
#
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         student_users = Student.objects.all()
#         for student in student_users:
#             user = student.user
#             tmp = user.last_name
#             user.last_name = user.first_name
#             user.first_name = tmp
#             user.save()
#         return Response(status=201)
#
#
# class SwapFirstAndLastNameFromTeacher(APIView):
#
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         teacher_users = User.objects.filter(user_role__role=TEACHER_ROLE)
#         for user in teacher_users:
#             tmp = user.last_name
#             user.last_name = user.first_name
#             user.first_name = tmp
#             user.save()
#         return Response(status=201)

#
# from django.conf import settings
# from portal.api.constants import TEACHER_DEFAULT_PASSWORD, TEACHER_ROLE
# import json
#
#
# class FetchTeachers(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#         user_pk = request.user.pk
#         path = settings.BASE_DIR + '\material_json\\teachers.txt'
#         # path = '/home/zhambyl/portal/backend/portal.django/src/material_json/teachers.txt'
#         f = open(path, 'r')
#         data_json = json.loads(f.read())
#         f.close()
#
#         print(data_json)
#
#         for item in data_json:
#             user = User(first_name=item['surname'],
#                         last_name=item['name'],
#                         username=item['username'])
#             user.set_password(TEACHER_DEFAULT_PASSWORD)
#             user.save()
#             UserRole(user=user, role=TEACHER_ROLE).save()
#             Staff(user=user, dob=item['dob']).save()
#         return Response(status=201)
#
#
# from django.conf import settings
# from portal.api.constants import STUDENT_DEFAULT_PASSWORD, STUDENT_ROLE, PARENT_ROLE
# from portal.api.utils import generate_random_username
# from .constants import RED, BLUE, GOLD
# import json
#
#
# class FetchStudents(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#         path = settings.BASE_DIR + '\material_json\\students.txt'
#         # path = '/home/zhambyl/portal/backend/portal.django/src/material_json/students.txt'
#         f = open(path, 'r')
#         data_json = json.loads(f.read())
#         f.close()
#
#         for item in data_json:
#             student_user = User(first_name=item['surname'],
#                                 last_name=item['name'],
#                                 username=item['username'])
#             student_user.set_password(STUDENT_DEFAULT_PASSWORD)
#             student_user.save()
#             UserRole(user=student_user, role=STUDENT_ROLE).save()
#             student = Student(user=student_user,
#                               grade=item['class'],
#                               phone=item['phone'],
#                               dob=item['dob'],
#                               school=item['school'],
#                               home_phone=item['home_phone'],
#                               target_subject=item['target_subject'],
#                               target_from=item['target_from'],
#                               instagram=item['instagram'])
#             if item['altyn_belgi'] == '1':
#                 student.certificate = GOLD
#             elif item['red'] == '1':
#                 student.certificate = RED
#             else:
#                 student.certificate = BLUE
#             student.save()
#
#         return Response(status=201)
#
#
# class FetchParents(APIView):
#
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#         path = settings.BASE_DIR + '\material_json\\parents.txt'
#         # path = '/home/zhambyl/portal/backend/portal.django/src/material_json/parents.txt'
#         f = open(path, 'r')
#         data_json = json.loads(f.read())
#         f.close()
#
#         for item in data_json:
#             try:
#                 student = Student.objects.get(user__username=item['username'])
#                 first_name = item['name']
#                 if item['name'] == '':
#                     first_name = 'Аты'
#
#                 last_name = item['surname']
#                 if item['surname'] == '':
#                     last_name = 'Тегі'
#
#                 username = generate_random_username()
#
#                 parent_user = User(first_name=first_name,
#                                    last_name=last_name,
#                                    username=username)
#                 parent_user.set_password('parent_password_'+username)
#                 parent_user.save()
#                 UserRole(user=parent_user, role=PARENT_ROLE).save()
#                 is_main = True if item['parent_order'] == '1' else False
#                 parent = Parent(user=parent_user,
#                                 student=student,
#                                 is_main=is_main,
#                                 phone=item['phone'])
#                 parent.save()
#             except Student.DoesNotExist:
#                 pass
#         return Response(status=201)
