from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from statuses.models import GroupStatus, LessonGroupStudentStatus
from materials.models import Topic, Subject
from portal.api.constants import WEEK_DAY_CHOICES, WEEK_DAY_SHORT_NAME
from userInfo.models import Staff


class Office(models.Model):
    title = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(Office, self).save()
        office_history = self.get_office_ent(changed_user_pk)
        office_history.is_deleted = False
        office_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        office_history = self.get_office_ent(changed_user_pk)
        office_history.is_deleted = True
        office_history.save()
        super(Office, self).delete()

    def get_office_ent(self, user_pk):
        return OfficeHistory(origin_id=self.pk,
                             changed_user_id=user_pk,
                             title=self.title,
                             created_date=self.created_date)


class Schedule(models.Model):
    office = models.ForeignKey(Office, on_delete=models.PROTECT)
    week_num = models.IntegerField(choices=WEEK_DAY_CHOICES)
    start_time = models.TimeField(auto_now_add=False, auto_now=False)
    finish_time = models.TimeField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['week_num', 'start_time', 'finish_time']
        unique_together = ['office', 'start_time', 'finish_time', 'week_num']

    def __str__(self):
        return str(self.office)+' '+str(self.week_num)+' '+str(self.start_time)+' '+str(self.finish_time)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(Schedule, self).save(*args, **kwargs)
        schedule_history = self.get_schedule_ent(changed_user_pk)
        schedule_history.is_deleted = False
        schedule_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        schedule_history = self.get_schedule_ent(changed_user_pk)
        schedule_history.is_deleted = True
        schedule_history.save()
        super(Schedule, self).delete()

    def get_schedule_ent(self, user_pk):
        return ScheduleHistory(origin_id=self.pk,
                               changed_user_id=user_pk,
                               office_id=self.office.pk,
                               week_num=self.week_num,
                               start_time=self.start_time,
                               finish_time=self.finish_time,
                               created_date=self.created_date)


class OfficeHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class ScheduleHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    office_id = models.IntegerField()
    week_num = models.IntegerField()
    start_time = models.TimeField(auto_now_add=False, auto_now=False)
    finish_time = models.TimeField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class LessonGroup(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # group_status = models.ForeignKey(GroupStatus, on_delete=models.PROTECT)
    title = models.CharField(max_length=120)
    student_limit = models.IntegerField()
    send_message_on_no_payment = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(LessonGroup, self).save(*args, **kwargs)
        lesson_group_history = self.get_lesson_group_ent(changed_user_pk)
        lesson_group_history.is_deleted = False
        lesson_group_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        lesson_group_history = self.get_lesson_group_ent(changed_user_pk)
        lesson_group_history.is_deleted = True
        lesson_group_history.save()
        super(LessonGroup, self).delete()

    def get_lesson_group_ent(self, user_pk):
        return LessonGroupHistory(origin_id=self.pk,
                                  changed_user_id=user_pk,
                                  teacher_id=self.teacher.pk,
                                  # group_status_id=self.group_status.pk,
                                  title=self.title,
                                  student_limit=self.student_limit,
                                  send_message_on_no_payment=self.send_message_on_no_payment,
                                  created_date=self.created_date)


class LessonGroupHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    teacher_id = models.IntegerField()
    # group_status_id = models.IntegerField()
    title = models.CharField(max_length=120)
    student_limit = models.IntegerField()
    send_message_on_no_payment = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class GroupSchedule(models.Model):
    lesson_group = models.OneToOneField(LessonGroup, on_delete=models.PROTECT, related_name="lg_group_schedule")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.lesson_group.title)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(GroupSchedule, self).save(*args, **kwargs)
        group_schedule_history = self.get_group_schedule_history_ent(changed_user_pk)
        group_schedule_history.is_deleted = False
        group_schedule_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        group_schedule_history = self.get_group_schedule_history_ent(changed_user_pk)
        group_schedule_history.is_deleted = False
        group_schedule_history.save()
        super(GroupSchedule, self).delete()

    def get_group_schedule_history_ent(self, user_id):
        return GroupScheduleHistory(origin_id=self.pk,
                                    changed_user_id=user_id,
                                    lesson_group_id=self.lesson_group.pk,
                                    created_date=self.created_date)


class GroupScheduleHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_id = models.IntegerField()
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']


class LessonGroupSchedule(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT, related_name='schedules')
    group_schedule = models.ForeignKey(GroupSchedule, on_delete=models.CASCADE, related_name='gs_lesson_group_schedule')

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(LessonGroupSchedule, self).save(*args, **kwargs)
        lesson_group_schedule_history = self.get_lesson_group_schedule_ent(changed_user_pk)
        lesson_group_schedule_history.is_deleted = False
        lesson_group_schedule_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        lesson_group_schedule_history = self.get_lesson_group_schedule_ent(changed_user_pk)
        lesson_group_schedule_history.is_deleted = True
        lesson_group_schedule_history.save()
        super(LessonGroupSchedule, self).delete()

    def get_lesson_group_schedule_ent(self, user_pk):
        return LessonGroupScheduleHistory(origin_id=self.pk,
                                          changed_user_id=user_pk,
                                          schedule_id=self.schedule.pk,
                                          group_schedule_id=self.group_schedule.pk)


class LessonGroupScheduleHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    schedule_id = models.IntegerField()
    group_schedule_id = models.IntegerField()
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)


class StudentPlan(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="s_student_plan")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['student', 'progress']

    def __str__(self):
        return self.student.last_name + ' ' + self.student.first_name + ' ('+self.subject.title+') '\
               + 'progress: ' + str(self.progress) + '%'

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(StudentPlan, self).save(*args, **kwargs)
        student_plan_history = self.get_student_plan_ent(changed_user_pk)
        student_plan_history.is_deleted = False
        student_plan_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        student_plan_history = self.get_student_plan_ent(changed_user_pk)
        student_plan_history.is_deleted = True
        student_plan_history.save()
        super(StudentPlan, self).delete()

    def get_student_plan_ent(self, user_pk):
        return StudentPlanHistory(origin_id=self.pk,
                                  changed_user_id=user_pk if user_pk else 1,
                                  student_id=self.student.pk,
                                  subject_id=self.subject.pk,
                                  progress=self.progress,
                                  created_date=self.created_date)


class StudentPlanHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField()
    student_id = models.IntegerField()
    subject_id = models.IntegerField()
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class SubjectPlan(models.Model):
    student_plan = models.ForeignKey(StudentPlan, on_delete=models.PROTECT, related_name="subject_plan")
    subject = models.ForeignKey(Subject, on_delete=models.Model)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-student_plan']

    def __str__(self):
        return self.student_plan.student.last_name+' '+self.student_plan.student.first_name\
               +' ('+self.student_plan.subject.title+') '+' "'+self.subject.title+'"'

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(SubjectPlan, self).save(*args, **kwargs)
        subject_plan_history = self.get_subject_plan_ent(changed_user_pk)
        subject_plan_history.is_deleted = False
        subject_plan_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        subject_plan_history = self.get_subject_plan_ent(changed_user_pk)
        subject_plan_history.is_deleted = True
        subject_plan_history.save()
        super(SubjectPlan, self).delete()

    def get_subject_plan_ent(self, user_pk):
        return SubjectPlanHistory(origin_id=self.pk,
                                  changed_user_id=user_pk if user_pk else 1,
                                  student_plan_id=self.student_plan.pk,
                                  subject_id=self.subject.pk,
                                  created_date=self.created_date)


class SubjectPlanHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField()
    student_plan_id = models.IntegerField()
    subject_id = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)


class TopicPlan(models.Model):
    subject_plan = models.ForeignKey(SubjectPlan, on_delete=models.PROTECT, related_name="topic_plan")
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="tp_topic")
    tutorial = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    class_work = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    home_work = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['subject_plan']

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(TopicPlan, self).save(*args, **kwargs)
        topic_plan_history = self.get_topic_plan_ent(changed_user_pk)
        topic_plan_history.is_deleted = False
        topic_plan_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        topic_plan_history = self.get_topic_plan_ent(changed_user_pk)
        topic_plan_history.is_deleted = True
        topic_plan_history.save()
        super(TopicPlan, self).delete()

    def get_topic_plan_ent(self, user_pk):
        return TopicPlanHistory(origin_id=self.pk,
                                changed_user_id=user_pk,
                                subject_plan_id=self.subject_plan.pk,
                                topic_id=self.topic.pk,
                                tutorial=self.tutorial,
                                class_work=self.class_work,
                                home_work=self.home_work,
                                created_date=self.created_date)


class TopicPlanHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    subject_plan_id = models.IntegerField()
    topic_id = models.IntegerField()
    tutorial = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    class_work = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    home_work = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class LessonGroupStudent(models.Model):
    student_plan = models.ForeignKey(StudentPlan, on_delete=models.PROTECT, related_name="sp_lesson_group_student")
    lesson_group = models.ForeignKey(LessonGroup, on_delete=models.PROTECT, related_name='lesson_group_plan')
    started_date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        student = self.student_plan.student
        return '{} {} {}'.format(self.lesson_group.title, student.last_name, student.first_name)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(LessonGroupStudent, self).save(*args, **kwargs)
        lesson_group_student_history = self.get_lesson_group_student_ent(changed_user_pk)
        lesson_group_student_history.is_deleted = False
        lesson_group_student_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        lesson_group_student_history = self.get_lesson_group_student_ent(changed_user_pk)
        lesson_group_student_history.is_deleted = True
        lesson_group_student_history.save()
        super(LessonGroupStudent, self).delete()

    def get_lesson_group_student_ent(self, user_pk):
        return LessonGroupStudentHistory(origin_id=self.pk,
                                         changed_user_id=user_pk,
                                         student_plan_id=self.student_plan.pk,
                                         lesson_group_id=self.lesson_group.pk,
                                         started_date=self.started_date,
                                         created_date=self.created_date)


class LessonGroupStudentHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    student_plan_id = models.IntegerField()
    lesson_group_id = models.IntegerField()
    started_date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class LessonGroupStudentShortSchedule(models.Model):
    lesson_group_student = models.ForeignKey(LessonGroupStudent, on_delete=models.CASCADE, related_name='short_schedule')
    week_day_sign = models.IntegerField(choices=WEEK_DAY_SHORT_NAME)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def save(self, *args, **kwargs):
        changed_user_id = kwargs.pop('user_pk', None)
        super(LessonGroupStudentShortSchedule, self).save(*args, **kwargs)
        lesson_group_student_short_schedule = self.get_lesson_group_student_short_schedule_history(changed_user_id)
        lesson_group_student_short_schedule.is_delete = False
        lesson_group_student_short_schedule.save()

    def delete(self, *args, **kwargs):
        changed_user_id = kwargs.pop('user_pk', None)
        lesson_group_student_short_schedule = self.get_lesson_group_student_short_schedule_history(changed_user_id)
        lesson_group_student_short_schedule.is_delete = True
        lesson_group_student_short_schedule.save()
        super(LessonGroupStudentShortSchedule, self).delete()

    def get_lesson_group_student_short_schedule_history(self, user_id):
        return LessonGroupStudentShortScheduleHistory(origin_id=self.pk,
                                                      changed_user_id=user_id,
                                                      lesson_group_student_id=self.lesson_group_student.pk,
                                                      week_day_sign=self.week_day_sign,
                                                      created_date=self.created_date)


class LessonGroupStudentShortScheduleHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_student_id = models.IntegerField()
    week_day_sign = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class MaterialAccessInfo(models.Model):
    lesson_group = models.ForeignKey(LessonGroup, on_delete=models.PROTECT, related_name="lg_material_access_info")
    accessed_ipv4 = models.CharField(max_length=15, null=True, blank=True)
    accessed_ipv6 = models.CharField(max_length=40, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['lesson_group']

    def __str__(self):
        return self.lesson_group.title

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(MaterialAccessInfo, self).save(*args, **kwargs)
        material_access_info = self.get_material_access_info(changed_user_pk)
        material_access_info.is_deleted = False
        material_access_info.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        material_access_info = self.get_material_access_info(changed_user_pk)
        material_access_info.is_deleted = True
        material_access_info.save()
        super(MaterialAccessInfo, self).delete()

    def get_material_access_info(self, user_pk):
        return MaterialAccessInfoHistory(origin_id=self.pk,
                                         changed_user_id=user_pk,
                                         lesson_group_id=self.lesson_group.pk,
                                         accessed_ipv4=self.accessed_ipv4,
                                         accessed_ipv6=self.accessed_ipv6,
                                         created_date=self.created_date)


class MaterialAccessInfoHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_id = models.IntegerField()
    accessed_ipv4 = models.CharField(max_length=15, null=True, blank=True)
    accessed_ipv6 = models.CharField(max_length=40, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class GroupReplacement(models.Model):
    lesson_group = models.ForeignKey(LessonGroup, on_delete=models.CASCADE, related_name="gr_lesson_group")
    teacher = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']
        unique_together = ['lesson_group', 'date']

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(GroupReplacement, self).save(*args, **kwargs)
        group_replacement_ent = self.get_group_replacement_history(changed_user_pk)
        group_replacement_ent.is_deleted = False
        group_replacement_ent.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        group_replacement_ent = self.get_group_replacement_history(changed_user_pk)
        group_replacement_ent.is_deleted = True
        group_replacement_ent.save()
        super(GroupReplacement, self).delete()

    def get_group_replacement_history(self, user_pk):
        return GroupReplacementHistory(origin_id=self.pk,
                                       changed_user_id=user_pk,
                                       lesson_group_id=self.lesson_group.pk,
                                       teacher_id=self.teacher.pk if self.teacher else None,
                                       date=self.date,
                                       created_date=self.created_date)


class GroupReplacementHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_id = models.IntegerField()
    teacher_id = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']


class DayOff(models.Model):
    date = models.DateField(auto_now_add=False, auto_now=False, unique=True)
    comment = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return '{} {}'.format(self.comment, str(self.date))

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(DayOff, self).save(*args, **kwargs)
        day_off_history = self.get_day_off_history(changed_user_pk)
        day_off_history.is_deleted = False
        day_off_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        day_off_history = self.get_day_off_history(changed_user_pk)
        day_off_history.is_deleted = True
        day_off_history.save()
        super(DayOff, self).delete()

    def get_day_off_history(self, user_pk):
        return DayOffHistory(origin_id=self.pk,
                             changed_user_id=user_pk,
                             date=self.date,
                             comment=self.comment,
                             created_date=self.created_date)


class DayOffHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=False, auto_now=False)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']
        

class GroupTimeTransfer(models.Model):
    lesson_group = models.ForeignKey(LessonGroup, on_delete=models.CASCADE, related_name='lg_group_time_transfer')
    from_date = models.DateField(auto_now_add=False, auto_now=False)
    to_date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    class Meta:
        unique_together = ['lesson_group', 'from_date']
    
    def __str__(self):
        return '{} From:{} To:{}'.format(self.lesson_group.title, str(self.from_date), str(self.to_date))
    
    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(GroupTimeTransfer, self).save(*args, **kwargs)
        group_time_transfer_history = self.get_group_time_transfer_history(changed_user_pk)
        group_time_transfer_history.is_deleted = False
        group_time_transfer_history.save()
    
    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        group_time_transfer_history = self.get_group_time_transfer_history(changed_user_pk)
        group_time_transfer_history.is_deleted = True
        group_time_transfer_history.save()
        super(GroupTimeTransfer, self).delete()
    
    def get_group_time_transfer_history(self, user_pk):
        return GroupTimeTransferHistory(origin_id=self.pk,
                                        changed_user_id=user_pk,
                                        lesson_group_id=self.lesson_group.pk,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                        created_date=self.created_date)
    

class GroupTimeTransferHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_id = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_date']
