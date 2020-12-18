from django.db import models
from django.conf import settings
from groupsAndLessons.models import LessonGroup, LessonGroupStudent, TopicPlan
from materials.models import Subject, Video, TopicTest, Topic


class TopicQuizMark(models.Model):
    topic_plan = models.ForeignKey(TopicPlan, on_delete=models.PROTECT, related_name="tqm_topic_plan")
    practice = models.IntegerField(null=True, blank=True)
    theory = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        changed_user_id = kwargs.pop('user_pk', None)
        super(TopicQuizMark, self).save(*args, **kwargs)
        topic_quiz_mark_history = self.get_topic_quiz_mark_ent(changed_user_id)
        topic_quiz_mark_history.is_delete = False
        topic_quiz_mark_history.save()

    def delete(self, *args, **kwargs):
        changed_user_id = kwargs.pop('user_pk', None)
        topic_quiz_mark_history = self.get_topic_quiz_mark_ent(changed_user_id)
        topic_quiz_mark_history.is_delete = True
        topic_quiz_mark_history.save()
        super(TopicQuizMark, self).delete()

    def get_topic_quiz_mark_ent(self, user_id):
        return TopicQuizMarkHistory(origin_id=self.pk,
                                    changed_user_id=user_id,
                                    topic_plan_id=self.topic_plan.pk,
                                    practice=self.practice,
                                    theory=self.theory,
                                    created_date=self.created_date)


class TopicQuizMarkHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    topic_plan_id = models.IntegerField()
    practice = models.IntegerField(null=True, blank=True)
    theory = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class GroupStudentVisit(models.Model):
    lesson_group = models.ForeignKey(LessonGroup, on_delete=models.PROTECT, related_name='lg_group_student_visit')
    abs_date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.lesson_group.title

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(GroupStudentVisit, self).save(*args, **kwargs)
        group_student_visit_history = self.get_group_student_visit_ent(changed_user_pk)
        group_student_visit_history.is_delete = False
        group_student_visit_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        group_student_visit_history = self.get_group_student_visit_ent(changed_user_pk)
        group_student_visit_history.is_delete = True
        group_student_visit_history.save()
        super(GroupStudentVisit, self).delete()

    def get_group_student_visit_ent(self, user_pk):
        return GroupStudentVisitHistory(origin_id=self.pk,
                                        changed_user_id=user_pk,
                                        lesson_group_id=self.lesson_group.pk,
                                        abs_date=self.abs_date,
                                        created_date=self.created_date)


class GroupStudentVisitHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_id = models.IntegerField()
    abs_date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class StudentVisit(models.Model):
    group_student_visit = models.ForeignKey(GroupStudentVisit, on_delete=models.PROTECT, related_name='group_student_visit')
    lesson_group_student = models.ForeignKey(LessonGroupStudent, on_delete=models.PROTECT, related_name='lgs_student_visit')
    attendance = models.BooleanField(default=False)
    home_work = models.DecimalField(max_digits=2, decimal_places=1)
    no_home_work = models.BooleanField(default=False)

    class Meta:
        ordering = ['group_student_visit']

    def __str__(self):
        student = self.lesson_group_student.student_plan.student
        return 'A: {}, HW: {}, NHW: {} {} {}'.format(str(self.attendance), str(self.home_work), str(self.no_home_work), student.last_name, student.first_name)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(StudentVisit, self).save(*args, **kwargs)
        student_visit_history = self.get_student_visit_ent(changed_user_pk)
        student_visit_history.is_deleted = False
        student_visit_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        student_visit_history = self.get_student_visit_ent(changed_user_pk)
        student_visit_history.is_deleted = True
        student_visit_history.save()
        super(StudentVisit, self).delete()

    def get_student_visit_ent(self, user_pk):
        return StudentVisitHistory(origin_id=self.pk,
                                   changed_user_id=user_pk,
                                   group_student_visit_id=self.group_student_visit.pk,
                                   lesson_group_student_id=self.lesson_group_student.pk,
                                   attendance=self.attendance,
                                   home_work=self.home_work,
                                   no_home_work=self.no_home_work)


class StudentVisitHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    group_student_visit_id = models.IntegerField()
    lesson_group_student_id = models.IntegerField()
    attendance = models.BooleanField(default=False)
    home_work = models.DecimalField(max_digits=2, decimal_places=1)
    no_home_work = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class TrialTest(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)

    class Meta:
        ordering = ['student', 'subject']

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(TrialTest, self).save(*args, **kwargs)
        trial_test_history = self.get_trial_test_history_ent(changed_user_pk)
        trial_test_history.is_deleted = False
        trial_test_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        trial_test_history = self.get_trial_test_history_ent(changed_user_pk)
        trial_test_history.is_deleted = True
        trial_test_history.save()
        super(TrialTest, self).delete()

    def get_trial_test_history_ent(self, user_id):
        return TrialTestHistory(origin_id=self.pk,
                                changed_user_id=user_id,
                                student_id=self.student.pk,
                                subject_id=self.subject.pk)


class TrialTestHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    student_id = models.IntegerField()
    subject_id = models.IntegerField()
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']


class TrialTestMark(models.Model):
    trial_test = models.ForeignKey(TrialTest, on_delete=models.PROTECT, related_name='ttm_trial_test')
    mark = models.IntegerField()
    date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(TrialTestMark, self).save(*args, **kwargs)
        trial_test_mark_history = self.get_trial_test_mark_ent(changed_user_pk)
        trial_test_mark_history.is_deleted = False
        trial_test_mark_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        trial_test_mark_history = self.get_trial_test_mark_ent(changed_user_pk)
        trial_test_mark_history.is_deleted = True
        trial_test_mark_history.save()
        super(TrialTestMark, self).delete()

    def get_trial_test_mark_ent(self, user_id):
        return TrialTestMarkHistory(origin_id=self.pk,
                                    changed_user_id=user_id,
                                    trial_test_id=self.trial_test.pk,
                                    mark=self.mark,
                                    date=self.date,
                                    created_date=self.created_date)


class TrialTestMarkHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    trial_test_id = models.IntegerField()
    mark = models.IntegerField()
    date = models.DateField(auto_now_add=False, auto_now=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class LessonVideoAction(models.Model):
    lesson_group_student = models.ForeignKey(LessonGroupStudent, on_delete=models.PROTECT, related_name="lgs_lesson_video_action")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(LessonVideoAction, self).save(*args, **kwargs)
        lesson_video_action_history = self.get_lesson_video_action_ent(changed_user_pk)
        lesson_video_action_history.is_deleted = False
        lesson_video_action_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        lesson_video_action_history = self.get_lesson_video_action_ent(changed_user_pk)
        lesson_video_action_history.is_deleted = True
        lesson_video_action_history.save()
        super(LessonVideoAction, self).delete()

    def get_lesson_video_action_ent(self, user_pk):
        return LessonVideoActionHistory(origin_id=self.pk,
                                        changed_user_id=user_pk,
                                        lesson_group_student_id=self.lesson_group_student.pk,
                                        topic_id=self.topic.pk,
                                        created_date=self.created_date)


class LessonVideoActionHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_student_id = models.IntegerField()
    topic_id = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class LessonTestAction(models.Model):
    lesson_group_student = models.ForeignKey(LessonGroupStudent, on_delete=models.PROTECT, related_name='lgs_lesson_test_action')
    test = models.ForeignKey(TopicTest, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(LessonTestAction, self).save(*args, **kwargs)
        lesson_test_action_history = self.get_lesson_test_action_ent(changed_user_pk)
        lesson_test_action_history.is_deleted = False
        lesson_test_action_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        lesson_test_action_history = self.get_lesson_test_action_ent(changed_user_pk)
        lesson_test_action_history.is_deleted = True
        lesson_test_action_history.save()
        super(LessonTestAction, self).delete()

    def get_lesson_test_action_ent(self, user_pk):
        return LessonTestActionHistory(origin_id=self.pk,
                                       changed_user_id=user_pk,
                                       lesson_group_student_id=self.lesson_group_student.pk,
                                       test_id=self.test.pk,
                                       created_date=self.created_date)


class LessonTestActionHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_student = models.IntegerField()
    test_id = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)
