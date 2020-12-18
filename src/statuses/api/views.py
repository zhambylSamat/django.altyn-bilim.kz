from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from portal.api.utils import permission
from django.contrib.auth.models import User

from ..models import UserStatus
from portal.api.constants import (
    DEVELOPER_ROLE,
    ADMIN_ROLE,
    SUPER_MODERATOR_ROLE,
    MODERATOR_ROLE,

    STUDENT_DEFAULT_PASSWORD,
    NO_PAYMENT_STATUS_PK
)
from portal.api.utils import (
    user_does_not_exists,
    revoke_token
)
from .serializers import UserStatusSerializer


class ResetStudentPasswordView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, user_pk):
        roles = (DEVELOPER_ROLE, ADMIN_ROLE, SUPER_MODERATOR_ROLE, MODERATOR_ROLE)
        permission(roles, request.user)

        try:
            student_user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return user_does_not_exists()

        student = student_user.user_student.get()
        if student.status is None:
            result = {'message': "User's password already reset!"}
            return Response(result, status=208)
        student.status = None
        student.save(user_pk=request.user.pk)
        student_user.is_active = False
        student_user.set_password(STUDENT_DEFAULT_PASSWORD)
        student_user.save()
        revoke_token(student_user.username)
        data = {
            'message': 'Password of ' + student_user.get_full_name() + ' successfully reset'
        }
        return Response(data, status=201)


class StudentNoPaymentStatusView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, user_pk):
        roles = (DEVELOPER_ROLE, ADMIN_ROLE, SUPER_MODERATOR_ROLE, MODERATOR_ROLE)
        permission(roles, request.user)

        try:
            student_user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return user_does_not_exists()

        try:
            no_payment_status = UserStatus.objects.get(pk=NO_PAYMENT_STATUS_PK)
        except UserStatus.DoesNotExist:
            data = {'message': 'no payment status does not exist'}
            return Response(data, status=404)

        try:
            student = student_user.user_student.get()
            student.status = no_payment_status
            student.save(user_pk=request.user.pk)
            student_user.is_active = no_payment_status.is_active
            student_user.save()
            revoke_token(student_user.username)
            data = {
                'message': 'Student status successfully changed to NO PAYMENT',
                'pk': NO_PAYMENT_STATUS_PK
            }
            return Response(data, status=201)
        except Exception:
            user_does_not_exists()
