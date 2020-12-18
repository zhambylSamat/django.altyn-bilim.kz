from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from portal.api.utils import permission
from portal.api.constants import FULL_STAFF_ROLES, DEVELOPER_ROLE

from ..models import LessonGroupIpConfiguration
from .serializers import SubjectQuizConfigurationSerializer
from .utils import reset_lesson_group_ip_configuration


class SubjectQuizConfigurationListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        subject_quiz_configuration = SubjectQuizConfigurationSerializer.objects.all()
        subject_quiz_configuration_serializer = SubjectQuizConfigurationSerializer(subject_quiz_configuration, many=True)
        return Response(subject_quiz_configuration_serializer.data, status=200)


class LessonGroupIPConfigurationDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        lesson_group_ip_configuration = LessonGroupIpConfiguration.objects.all().first()
        result = {'is_access_with_ip': False}
        if lesson_group_ip_configuration is None:
            return Response(result, status=200)
        result['is_access_with_ip'] = lesson_group_ip_configuration.is_checking_ip
        return Response(result, status=200)

    def post(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        lesson_group_ip_configuration = LessonGroupIpConfiguration.objects.all().first()
        if lesson_group_ip_configuration is not None:
            lesson_group_ip_configuration.is_checking_ip = False
            lesson_group_ip_configuration.save(user_pk=request.user.pk)
        else:
            lesson_group_ip_configuration = LessonGroupIpConfiguration(is_checking_ip=False)
            lesson_group_ip_configuration.save(user_pk=request.user.pk)
        return Response(status=201)

    def put(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        lesson_group_ip_configuration = LessonGroupIpConfiguration.objects.all().first()
        if lesson_group_ip_configuration is not None:
            lesson_group_ip_configuration.is_checking_ip = True
            lesson_group_ip_configuration.save(user_pk=request.user.pk)
        else:
            lesson_group_ip_configuration = LessonGroupIpConfiguration(is_checking_ip=True)
            lesson_group_ip_configuration.save(user_pk=request.user.pk)
        return Response(status=201)


class ResetLessonGroupIpConfigurationView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = (DEVELOPER_ROLE,)
        permission(roles, request.user)
        reset_lesson_group_ip_configuration()
        return Response(status=201)

