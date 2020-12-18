from lessonProgress.models import GroupStudentVisit, StudentVisit, TrialTestMark
from configuration.models import SubjectQuizConfiguration, SubjectQuizMarkConfiguration, TrialTestMarkConfiguration
from django.db.models import Q
from .constants import (
    TWO_DAY_ABS,
    RE_RETAKE_QUIZ,
    NO_HOME_WORK,
    EXCELLENT_QUIZ,
    MAX_QUIZ,
    MAX_TRIAL_TEST,
    THREE_TIMES_UP_TRIAL_TEST,

    notification_type_count,

    SUCCESS_CLASS,
    DANGER_CLASS,
)
from ..models import Notification
import datetime


def create_new_notification(notification_type, notification_class, notification_count,
                            extra_object_id, extra_object_app_name, extra_object_model_name,
                            object_id, object_app_name, object_model_name):
    new_notification = Notification(notification_type=notification_type,
                                    notification_class=notification_class,
                                    notification_count=notification_count,
                                    extra_object_id=extra_object_id,
                                    extra_object_app_name=extra_object_app_name,
                                    extra_object_model_name=extra_object_model_name,
                                    object_id=object_id,
                                    object_app_name=object_app_name,
                                    object_model_name=object_model_name)
    new_notification.save()


def student_attendance_notification():# run at 00:59 # fake_date=None
    # fake_date = datetime.datetime.strptime(fake_date, '%Y-%m-%d')  # 01:59:00.000000  %H:%M:%S.%f
    # fake_date.replace(hour=1, minute=59, second=0, microsecond=0)
    # print(fake_date)
    now = datetime.datetime.now() - datetime.timedelta(hours=1)
    # now = fake_date - datetime.timedelta(hours=1)
    yesterday = now - datetime.timedelta(days=1)
    group_student_visit_list = GroupStudentVisit.objects.filter(Q(created_date__lte=now)
                                                                & Q(created_date__gt=yesterday)).order_by('created_date')
    for group_student in group_student_visit_list:
        student_visit_list = StudentVisit.objects.filter(group_student_visit=group_student)
        for student_visit in student_visit_list:
            extra_object_model_name = student_visit.lesson_group_student.__class__.__name__
            extra_object_app_name = student_visit.lesson_group_student._meta.app_label
            object_model_name = student_visit.__class__.__name__
            object_app_name = student_visit._meta.app_label
            # extra_object_id is lesson_group_student__pk
            notification = Notification.objects.filter(Q(notification_type=TWO_DAY_ABS)
                                                       & Q(extra_object_id=student_visit.lesson_group_student.pk)) \
                .order_by('-created_date')[:notification_type_count(TWO_DAY_ABS)]
            if not student_visit.attendance:
                if notification.count() == 0 or notification[0].notification_count == notification_type_count(TWO_DAY_ABS):
                    create_new_notification(TWO_DAY_ABS, DANGER_CLASS, 1,
                                            student_visit.lesson_group_student.pk, extra_object_app_name, extra_object_model_name,
                                            student_visit.pk, object_app_name, object_model_name)
                else:
                    get_last_notification_count = notification[0].notification_count
                    create_new_notification(TWO_DAY_ABS, DANGER_CLASS, get_last_notification_count + 1,
                                            student_visit.lesson_group_student.pk, extra_object_app_name, extra_object_model_name,
                                            student_visit.pk, object_app_name, object_model_name)
            else:
                if student_visit.home_work == 0.0 and not student_visit.no_home_work:
                    create_new_notification(NO_HOME_WORK, DANGER_CLASS, 1,
                                            student_visit.lesson_group_student.pk, extra_object_app_name, extra_object_model_name,
                                            student_visit.pk, object_app_name, object_model_name)
                if notification.count() > 0 and notification[0].notification_count != notification_type_count(TWO_DAY_ABS):
                    notification[0].delete()


def topic_quiz_max_mark_check_in_notification(topic_quiz_mark):
    try:
        Notification.objects.get(object_id=topic_quiz_mark.pk)
    except Notification.DoesNotExist:
        extra_object_model_name = topic_quiz_mark.topic_plan.__class__.__name__
        extra_object_app_name = topic_quiz_mark.topic_plan._meta.app_label
        object_model_name = topic_quiz_mark.__class__.__name__
        object_app_name = topic_quiz_mark._meta.app_label
        create_new_notification(MAX_QUIZ, SUCCESS_CLASS, 1,
                                topic_quiz_mark.topic_plan.pk, extra_object_app_name, extra_object_model_name,
                                topic_quiz_mark.pk, object_app_name, object_model_name)


def topic_quiz_max_mark(topic_quiz_mark, subject_quiz_configuration):
    if subject_quiz_configuration.is_practice and subject_quiz_configuration.is_theory:
        if topic_quiz_mark.practice == 100 and topic_quiz_mark.theory == 100:
            topic_quiz_max_mark_check_in_notification(topic_quiz_mark)
            return True
    elif subject_quiz_configuration.is_practice and topic_quiz_mark.practice == 100:
        topic_quiz_max_mark_check_in_notification(topic_quiz_mark)
        return True
    elif subject_quiz_configuration.is_theory and topic_quiz_mark.theory == 100:
        topic_quiz_max_mark_check_in_notification(topic_quiz_mark)
        return True
    return False


def topic_quiz_excellent_mark_check_in_notification(topic_quiz_mark):
    try:
        Notification.objects.get(object_id=topic_quiz_mark.pk)
    except Notification.DoesNotExist:
        extra_object_model_name = topic_quiz_mark.topic_plan.__class__.__name__
        extra_object_app_name = topic_quiz_mark.topic_plan._meta.app_label
        object_model_name = topic_quiz_mark.__class__.__name__
        object_app_name = topic_quiz_mark._meta.app_label
        create_new_notification(EXCELLENT_QUIZ, SUCCESS_CLASS, 1,
                                topic_quiz_mark.topic_plan.pk, extra_object_app_name, extra_object_model_name,
                                topic_quiz_mark.pk, object_app_name, object_model_name)


def topic_quiz_excellent_mark(topic_quiz_mark, subject_quiz_configuration, excellent_mark):
    if subject_quiz_configuration.is_practice and subject_quiz_configuration.is_theory:
        if excellent_mark <= topic_quiz_mark.practice < 100 and excellent_mark <= topic_quiz_mark.theory < 100:
                topic_quiz_excellent_mark_check_in_notification(topic_quiz_mark)
    elif subject_quiz_configuration.is_practice and excellent_mark <= topic_quiz_mark.practice < 100:
        topic_quiz_excellent_mark_check_in_notification(topic_quiz_mark)
    elif subject_quiz_configuration.is_theory and excellent_mark <= topic_quiz_mark.theory < 100:
        topic_quiz_excellent_mark_check_in_notification(topic_quiz_mark)


def topic_quiz_retake_mark_check_in_notification(topic_quiz_mark):
    try:
        Notification.objects.get(object_id=topic_quiz_mark.pk)
    except Notification.DoesNotExist:
        extra_object_model_name = topic_quiz_mark.topic_plan.__class__.__name__
        extra_object_app_name = topic_quiz_mark.topic_plan._meta.app_label
        object_model_name = topic_quiz_mark.__class__.__name__
        object_app_name = topic_quiz_mark._meta.app_label
        notification_list = Notification.objects.filter(extra_object_id=topic_quiz_mark.topic_plan.pk) \
                                .order_by('-created_date')[:notification_type_count(RE_RETAKE_QUIZ)]
        if notification_list.count() == 0:
            create_new_notification(RE_RETAKE_QUIZ, DANGER_CLASS, 1,
                                    topic_quiz_mark.topic_plan.pk, extra_object_app_name, extra_object_model_name,
                                    topic_quiz_mark.pk, object_app_name, object_model_name)
        else:
            last_notification_count = notification_list[0].notification_count
            create_new_notification(RE_RETAKE_QUIZ, DANGER_CLASS, last_notification_count + 1,
                                    topic_quiz_mark.topic_plan.pk, extra_object_app_name, extra_object_model_name,
                                    topic_quiz_mark.pk, object_app_name, object_model_name)


def topic_quiz_retake_mark(topic_quiz_mark_list, subject_quiz_configuration, retake_mark):
    if subject_quiz_configuration.is_practice and subject_quiz_configuration.is_theory:
        if (topic_quiz_mark_list[0].practice <= retake_mark or topic_quiz_mark_list[0].theory <= retake_mark) \
                and (topic_quiz_mark_list[1].practice <= retake_mark or topic_quiz_mark_list[1].theory <= retake_mark):
            topic_quiz_retake_mark_check_in_notification(topic_quiz_mark_list[1])
            topic_quiz_retake_mark_check_in_notification(topic_quiz_mark_list[0])
    elif subject_quiz_configuration.is_practice:
        if topic_quiz_mark_list[0].practice <= retake_mark and topic_quiz_mark_list[1].practice <= retake_mark:
            topic_quiz_retake_mark_check_in_notification(topic_quiz_mark_list[1])
            topic_quiz_retake_mark_check_in_notification(topic_quiz_mark_list[0])
    elif subject_quiz_configuration.is_theory:
        if topic_quiz_mark_list[0].theory <= retake_mark and topic_quiz_mark_list[1].theory <= retake_mark:
            topic_quiz_retake_mark_check_in_notification(topic_quiz_mark_list[1])
            topic_quiz_retake_mark_check_in_notification(topic_quiz_mark_list[0])


def topic_quiz_notification():# run at 01:29 # fake_date=None
    # fake_date = datetime.datetime.strptime(fake_date, '%Y-%m-%d')  # 01:59:00.000000  %H:%M:%S.%f
    # fake_date.replace(hour=1, minute=59, second=0, microsecond=0)
    # print(fake_date)
    now = datetime.datetime.now() - datetime.timedelta(hours=1, minutes=30)
    # now = fake_date - datetime.timedelta(hours=1, minutes=30)
    yesterday = now - datetime.timedelta(days=1)
    min_date = datetime.datetime.strptime('2020-03-01 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
    group_student_visit_list = GroupStudentVisit.objects.filter(Q(created_date__lte=now)
                                                                & Q(created_date__gt=yesterday)).order_by('created_date')
    subject_quiz_configuration_list = SubjectQuizConfiguration.objects.all()
    subject_quiz_mark_configuration_list = SubjectQuizMarkConfiguration.objects.all()
    # extra_object_id is topic_plan__pk
    for group_student in group_student_visit_list:
        student_visit_list = StudentVisit.objects.filter(group_student_visit=group_student)
        for student_visit in student_visit_list:
            if student_visit.attendance:
                subject_plan_list = student_visit.lesson_group_student.student_plan.subject_plan.all()
                for subject_plan in subject_plan_list:
                    topic_plan_list = subject_plan.topic_plan.filter(topic__is_mid_control=True)
                    subject_quiz_configuration = subject_quiz_configuration_list.get(subject=subject_plan.subject)
                    subject_quiz_mark_configuration = subject_quiz_mark_configuration_list.get(subject=subject_plan.subject)
                    for topic_plan in topic_plan_list:
                        topic_quiz_mark_list = topic_plan.tqm_topic_plan.filter(Q(created_date__lt=group_student.created_date)
                                                                                &Q(created_date__gte=min_date)).order_by('-created_date')
                        if len(topic_quiz_mark_list) == 1:
                            if topic_quiz_max_mark(topic_quiz_mark_list[0],
                                                   subject_quiz_configuration):
                                pass
                            else:
                                topic_quiz_excellent_mark(topic_quiz_mark_list[0],
                                                          subject_quiz_configuration,
                                                          subject_quiz_mark_configuration.excellent_mark)
                        elif len(topic_quiz_mark_list) == 2:
                            topic_quiz_retake_mark(topic_quiz_mark_list,
                                                   subject_quiz_configuration,
                                                   subject_quiz_mark_configuration.retake_mark)


def trial_test_max_mark(trial_test_mark, good_mark):
    if trial_test_mark.mark >= good_mark:
        try:
            Notification.objects.get(Q(object_id=trial_test_mark.pk)
                                     & Q(notification_type=MAX_TRIAL_TEST))
        except Notification.DoesNotExist:
            extra_object_model_name = trial_test_mark.trial_test.__class__.__name__
            extra_object_app_name = trial_test_mark.trial_test._meta.app_label
            object_model_name = trial_test_mark.__class__.__name__
            object_app_name = trial_test_mark._meta.app_label
            create_new_notification(MAX_TRIAL_TEST, SUCCESS_CLASS, 1,
                                    trial_test_mark.trial_test.pk, extra_object_app_name, extra_object_model_name,
                                    trial_test_mark.pk, object_app_name, object_model_name)


def trial_test_increase_mark(trial_test_mark_list, bad_mark):
    is_ok = True
    last_mark = 0
    trial_test_mark_pk_list = []
    for trial_test_mark in trial_test_mark_list:
        if trial_test_mark.mark <= bad_mark:
            is_ok = False
            break
        else:
            if trial_test_mark.mark < last_mark or last_mark == 0:
                last_mark = trial_test_mark.mark
                trial_test_mark_pk_list.append(trial_test_mark.pk)
            else:
                is_ok = False
                break
    if is_ok:
        notification_list = Notification.objects.filter(Q(object_id__in=trial_test_mark_pk_list)
                                                        & Q(notification_type=THREE_TIMES_UP_TRIAL_TEST))
        if notification_list.count() == 0:
            count = 0
            for trial_test_mark in trial_test_mark_list:
                extra_object_app_name = trial_test_mark.trial_test._meta.app_label
                extra_object_model_name = trial_test_mark.trial_test.__class__.__name__
                object_app_name = trial_test_mark._meta.app_label
                object_model_name = trial_test_mark.__class__.__name__
                count += 1
                create_new_notification(THREE_TIMES_UP_TRIAL_TEST, SUCCESS_CLASS, count,
                                        trial_test_mark.trial_test.pk, extra_object_app_name, extra_object_model_name,
                                        trial_test_mark.pk, object_app_name, object_model_name)


def trial_test_notification():# run at 01:59 # fake_date=None
    # fake_date = datetime.datetime.strptime(fake_date, '%Y-%m-%d') # 01:59:00.000000  %H:%M:%S.%f
    # fake_date.replace(hour=1, minute=59, second=0, microsecond=0)
    # print(fake_date)
    now = datetime.datetime.now() - datetime.timedelta(hours=2)
    # now = fake_date - datetime.timedelta(hours=2)
    yesterday = now - datetime.timedelta(days=1)
    min_date = datetime.datetime.strptime('2019-04-30 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
    group_student_visit_list = GroupStudentVisit.objects.filter(Q(created_date__lte=now)
                                                                & Q(created_date__gt=yesterday)).order_by('created_date')
    trial_test_mark_config_list = TrialTestMarkConfiguration.objects.all()
    # extra_object_id is trial_test__pk
    for group_student in group_student_visit_list:
        student_visit_list = StudentVisit.objects.filter(group_student_visit=group_student)
        for student_visit in student_visit_list:
            if student_visit.attendance:
                student_plan = student_visit.lesson_group_student.student_plan
                subject_plan_list = student_plan.subject_plan.all()
                for subject_plan in subject_plan_list:
                    trial_test_mark_list = TrialTestMark.objects.filter(Q(trial_test__subject=subject_plan.subject)
                                                                        & Q(trial_test__student=student_plan.student)
                                                                        & Q(created_date__lt=group_student.abs_date)
                                                                        & Q(created_date__gte=min_date)).order_by('-created_date')[:3]
                    trial_test_mark_config = trial_test_mark_config_list.get(subject=subject_plan.subject)
                    if trial_test_mark_list.count() > 0:
                        trial_test_max_mark(trial_test_mark_list[0], trial_test_mark_config.good_mark)
                    if trial_test_mark_list.count() == 3:
                        trial_test_increase_mark(trial_test_mark_list,
                                                 trial_test_mark_config.bad_mark)

