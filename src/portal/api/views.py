from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .constants import (
    FIELDS_FILLED_WRONG,
    ROLES_INFO,
    FULL_STAFF_ROLES,
    TEACHER_ROLE,
    STUDENT_ROLE,
    DEVELOPER_ROLE
)
from .utils import get_user_response
from .utils import (
    wrong_username_or_password,
    permission,
    revoke_token
)
from .serializer import (
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerilizer
)
from django.core.mail import send_mail
from portal.settings import DEFAULT_FROM_EMAIL


class StaffAuthView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        result = {'errors': []}
        if login_serializer.is_valid():
            username = login_serializer.data['username'].lower()
            password = login_serializer.data['password']
            try:
                user = User.objects.get(username=username)
                roles = FULL_STAFF_ROLES
                permission(roles, user)
            except User.DoesNotExist:
                return wrong_username_or_password()
            if user.is_active and check_password(password, user.password):
                if user.user_staff.get().is_password_reset:
                    user_serializer = UserSerializer(user, many=False)
                    return Response(user_serializer.data, status=202)
                else:
                    result = get_user_response(user, login_serializer.data['password'])
                    return Response(result, status=200)
        else:
            result['errors'].append(login_serializer.errors)
        result['errors'].append(FIELDS_FILLED_WRONG)
        return Response(result, status=400)


class StaffChangePasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        change_password_serializer = ChangePasswordSerilizer(data=request.data.copy(), many=False)
        error = {'message': []}
        
        if change_password_serializer.is_valid():
            user = User.objects.get(pk=change_password_serializer.data['user'])
            user.set_password(change_password_serializer.data['new_password'])
            user.save()
            staff = user.user_staff.get()
            staff.is_password_reset = False
            staff.save(user_pk=user.pk)
            revoke_token(user.username)
            result = get_user_response(user, change_password_serializer.data['new_password'])
            return Response(result, status=200)
        else:
            error['message'].append(change_password_serializer.errors)
            return Response(error, status=400)


class TeacherAuthView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        result = {'errors': []}
        if login_serializer.is_valid():
            username = login_serializer.data['username'].lower()
            password = login_serializer.data['password']
            try:
                user = User.objects.get(username=username)
                roles = TEACHER_ROLE
                permission(roles, user)
            except User.DoesNotExist:
                return wrong_username_or_password()
            if user.is_active and check_password(password, user.password):
                if user.user_staff.get().is_password_reset:
                    user_serializer = UserSerializer(user, many=False)
                    return Response(user_serializer.data, status=202)
                else:
                    result = get_user_response(user, login_serializer.data['password'])
                    return Response(result, status=200)
        else:
            result['errors'].append(login_serializer.errors)
        result['errors'].append(FIELDS_FILLED_WRONG)
        return Response(result, status=400)


class StudentAuthView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data.copy())
        result = {'errors': []}
        if login_serializer.is_valid():
            username = login_serializer.data['username'].lower()
            password = login_serializer.data['password']
            try:
                user = User.objects.get(username=username)
                roles = STUDENT_ROLE
                permission(roles, user)
            except User.DoesNotExist:
                return wrong_username_or_password()
            if user.is_active and check_password(password, user.password):
                student = user.user_student.get()
                if student.has_payment and student.has_contract:
                    if student.is_password_reset:
                        user_serializer = UserSerializer(user, many=False)
                        return Response(user_serializer.data, status=202)
                    result = get_user_response(user, login_serializer.data['password'])
                    return Response(result, status=200)
                elif not student.has_payment or not student.has_contract:
                    result = {
                        'message': []
                    }
                    if not student.has_payment:
                        result['message'].append('Оплата төленбеген Администрацияға жолығыңыз!')
                    if not student.has_contract:
                        result['message'].append('Договор өткізілмеген Администрацияға жолығыңыз!')
                    return Response(result, status=203)
        else:
            result['errors'].append(login_serializer.errors)
        result['errors'].append(FIELDS_FILLED_WRONG)
        return Response(result, status=400)


class StudentChangePasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        change_password_serializer = ChangePasswordSerilizer(data=request.data.copy(), many=False)
        error = {'message': []}

        if change_password_serializer.is_valid():
            user = User.objects.get(pk=change_password_serializer.data['user'])
            user.set_password(change_password_serializer.data['new_password'])
            user.save()
            student = user.user_student.get()
            student.is_password_reset = False
            student.save(user_pk=user.pk)
            revoke_token(user.username)
            result = get_user_response(user, change_password_serializer.data['new_password'])
            return Response(result, status=200)
        else:
            error['message'].append(change_password_serializer.errors)
            return Response(error, status=400)


class RoleListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        result = []
        roles_header = ROLES_INFO[0]
        for i in range(1, len(ROLES_INFO)):
            tmp = {}
            for j in range(len(roles_header)):
                tmp[roles_header[j]] = ROLES_INFO[i][j]
            result.append(tmp)
        return JsonResponse(result, safe=False)


class RequestFromClientView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        subject = 'Клинет оставил заявку'
        message = 'имя: {}, телефон {}'.format(request.data['name'], request.data['phone'])
        from_mail = DEFAULT_FROM_EMAIL
        to_mail = ['zhambyl.9670@gmail.com']
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        return Response(status=201)
