from groupsAndLessons.models import GroupSchedule, LessonGroupSchedule, MaterialAccessInfo
from configuration.models import LessonGroupIpConfiguration
import datetime
from django.db.models import Q
from ..models import LessonVideoAction
from django.contrib.auth.models import User


def get_day_sign_by_num(day_num):
    if day_num in [1, 2]:
        return 1
    elif day_num in [3, 4]:
        return 2
    elif day_num in [5, 6]:
        return 3
    return None


def has_access_to_video(lesson_group):
    group_schedule = GroupSchedule.objects.get(lesson_group=lesson_group)
    today = datetime.datetime.now()
    week_num = today.strftime('%w')
    return True
    try:
        lesson_group_schedule = LessonGroupSchedule.objects.get(Q(group_schedule=group_schedule)
                                                                & Q(schedule__week_num=week_num))
        schedule = lesson_group_schedule.schedule
        start_time = (today + datetime.timedelta(minutes=30)).time()
        finish_time = (today - datetime.timedelta(minutes=30)).time()
        return start_time >= schedule.start_time and finish_time <= schedule.finish_time
    except LessonGroupSchedule.DoesNotExist:
        return False


def get_ip_from_meta(meta):

    # ip = meta['HTTP_X_REAL_IP']
    ip = '127.0.0.1'
    return ip


def set_ip(lesson_group, meta, user_pk):

    ip = get_ip_from_meta(meta)
    try:
        material_access_info = MaterialAccessInfo.objects.get(lesson_group=lesson_group)
        material_access_info.delete(user_pk=user_pk)
    except MaterialAccessInfo.DoesNotExist:
        pass
    material_access_info = MaterialAccessInfo(lesson_group=lesson_group,
                                              accessed_ipv4=ip)
    material_access_info.save(user_pk=user_pk)


def check_ip(lesson_group, meta):

    lesson_group_ip_configuration = LessonGroupIpConfiguration.objects.all().first()

    if lesson_group_ip_configuration is not None and not lesson_group_ip_configuration.is_checking_ip:
        return True

    ip = get_ip_from_meta(meta)
    try:
        material_access_info = MaterialAccessInfo.objects.get(lesson_group=lesson_group)
        if material_access_info.accessed_ipv4 == ip:
            return True
        return False
    except MaterialAccessInfo.DoesNotExist:
        return False


def remove_all_student_video_access():
    try:
        system_user_pk = User.objects.get(username='system').pk
    except User.DoesNotExist:
        system_user_pk = None
    lesson_video_action_list = LessonVideoAction.objects.all()
    for lesson_video_action in lesson_video_action_list:
        lesson_video_action.delete(user_pk=system_user_pk)
