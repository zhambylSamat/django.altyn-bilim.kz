from django.db import models
from materials.models import Subject


class TrialTestMarkConfiguration(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    max_mark = models.IntegerField()
    good_mark = models.IntegerField()
    bad_mark = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return '{} max: {} good: {} bad: {}'. format(self.subject.title, self.max_mark, self.good_mark, self.bad_mark)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(TrialTestMarkConfiguration, self).save(*args, **kwargs)
        trial_test_mark_configuration_history = self.get_trial_test_mark_configuration_ent(changed_user_pk)
        trial_test_mark_configuration_history.is_deleted = False
        trial_test_mark_configuration_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        trial_test_mark_configuration_history = self.get_trial_test_mark_configuration_ent(changed_user_pk)
        trial_test_mark_configuration_history.is_deleted = True
        trial_test_mark_configuration_history.save()
        super(TrialTestMarkConfiguration, self).delete()

    def get_trial_test_mark_configuration_ent(self, user_id):
        return TrialTestMarkConfigurationHistory(origin_id=self.id,
                                                 changed_user_id=user_id,
                                                 subject_id=self.subject.pk,
                                                 max_mark=self.max_mark,
                                                 good_mark=self.good_mark,
                                                 bad_mark=self.bad_mark,
                                                 created_date=self.created_date)


class TrialTestMarkConfigurationHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    subject_id = models.IntegerField()
    max_mark = models.IntegerField()
    good_mark = models.IntegerField()
    bad_mark = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class SubjectQuizConfiguration(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    is_practice = models.BooleanField(default=False)
    is_theory = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    class Meta:
        ordering = ['-created_date']
        
    def __str__(self):
        return self.subject.title
    
    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(SubjectQuizConfiguration, self).save(*args, **kwargs)
        subject_quiz_configuration_history = self.get_subject_quiz_configuration_ent(changed_user_pk)
        subject_quiz_configuration_history.is_deleted = False
        subject_quiz_configuration_history.save()
    
    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        subject_quiz_configuration_history = self.get_subject_quiz_configuration_ent(changed_user_pk)
        subject_quiz_configuration_history.is_deleted = True
        subject_quiz_configuration_history.save()
        super(SubjectQuizConfiguration, self).delete()
    
    def get_subject_quiz_configuration_ent(self, user_id):
        return SubjectQuizConfigurationHistory(origin_id=self.pk,
                                               changed_user_id=user_id,
                                               subject_id=self.subject_id,
                                               is_practice=self.is_practice,
                                               is_theory=self.is_theory,
                                               created_date=self.created_date)
    

class SubjectQuizConfigurationHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    subject_id = models.IntegerField()
    is_practice = models.BooleanField(default=False)
    is_theory = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-updated_date']
        
    def __str__(self):
        return str(self.origin_id)


class LessonGroupIpConfiguration(models.Model):
    is_checking_ip = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(LessonGroupIpConfiguration, self).save(*args, **kwargs)
        lesson_group_ip_configuration = self.get_lesson_group_ip_configuration(changed_user_pk)
        lesson_group_ip_configuration.is_deleted = False
        lesson_group_ip_configuration.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        lesson_group_ip_configuration = self.get_lesson_group_ip_configuration(changed_user_pk)
        lesson_group_ip_configuration.is_deleted = True
        lesson_group_ip_configuration.save()
        super(LessonGroupIpConfiguration, self).delete()

    def get_lesson_group_ip_configuration(self, user_id):
        return LessonGroupIpConfigurationHistory(origin_id=self.pk,
                                                 changed_user_id=user_id,
                                                 is_checking_ip=self.is_checking_ip,
                                                 created_date=self.created_date)


class LessonGroupIpConfigurationHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    is_checking_ip = models.BooleanField(default=True)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class SubjectQuizMarkConfiguration(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    retake_mark = models.IntegerField()
    excellent_mark = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(SubjectQuizMarkConfiguration, self).save(*args, **kwargs)
        subject_quiz_mark_configuration_history = self.get_subject_quiz_mark_configuration_history_ent(changed_user_pk)
        subject_quiz_mark_configuration_history.is_deleted = False
        subject_quiz_mark_configuration_history.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        subject_quiz_mark_configuration_history = self.get_subject_quiz_mark_configuration_history_ent(changed_user_pk)
        subject_quiz_mark_configuration_history.is_deleted = True
        subject_quiz_mark_configuration_history.save(*args, **kwargs)
        super(SubjectQuizMarkConfiguration, self).delete()

    def get_subject_quiz_mark_configuration_history_ent(self, user_id):
        return SubjectQuizMarkConfigurationHistory(origin_id=self.pk,
                                                   changed_user_id=user_id,
                                                   subject_id=self.subject.pk,
                                                   retake_mark=self.retake_mark,
                                                   excellent_mark=self.excellent_mark,
                                                   created_date=self.created_date)


class SubjectQuizMarkConfigurationHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    subject_id = models.IntegerField()
    retake_mark = models.IntegerField()
    excellent_mark = models.IntegerField()
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']
