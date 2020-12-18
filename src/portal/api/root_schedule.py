from django_cron import CronJobBase, Schedule
from configuration.api.utils import reset_lesson_group_ip_configuration
from lessonProgress.api.utils import remove_all_student_video_access
from notificationAndPrize.api.utils import (
    student_attendance_notification, # run at 00:59
    topic_quiz_notification, # run at 01:29
    trial_test_notification # run at 01:59
)


class ResetPortalConfiguration(CronJobBase):
    RUN_AT_TIMES = ['21:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'portal.api.cron'    # a unique code

    def do(self):
        reset_lesson_group_ip_configuration()
        remove_all_student_video_access()


class StudentAttendanceNotification(CronJobBase):
    RUN_AT_TIMES = ['00:59']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'portal.api.studentAttendanceNotification'

    def do(self):
        student_attendance_notification()


class TopicQuizNotification(CronJobBase):
    RUN_AT_TIMES = ['01:29']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'portal.api.topicQuizNotification'

    def do(self):
        topic_quiz_notification()


class TrialTestNotification(CronJobBase):
    RUN_AT_TIMES = ['01:59']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'portal.api.trialTestNotification'

    def do(self):
        trial_test_notification()
