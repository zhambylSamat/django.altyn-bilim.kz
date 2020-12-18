from ..models import LessonGroupIpConfiguration
from django.contrib.auth.models import User


def reset_lesson_group_ip_configuration():
    lesson_group_ip_configuration = LessonGroupIpConfiguration.objects.all().first()
    lesson_group_ip_configuration.is_checking_ip = True
    try:
        system_user_pk = User.objects.get(username='system').pk
    except User.DoesNotExist:
        system_user_pk = None
    lesson_group_ip_configuration.save(user_pk=system_user_pk)
