from django.db import models
from django.conf import settings


class UserStatus(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super(UserStatus, self).save(*args, *kwargs)
        user_status_history = self.get_user_status_ent()
        user_status_history.is_deleted = False
        user_status_history.save()

    def delete(self, *args):
        user_status_history = self.get_user_status_ent()
        user_status_history.is_deleted = True
        user_status_history.save()
        super(UserStatus, self).delete()

    def get_user_status_ent(self, user_pk=None):
        return UserStatusHistory(origin_id=self.pk,
                                 changed_user_id=user_pk,
                                 title=self.title,
                                 description=self.description,
                                 is_active=self.is_active,
                                 created_date=self.created_date)


class UserStatusHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class GroupStatus(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(GroupStatus, self).save(*args, **kwargs)
        group_student_history = self.get_group_status_ent(changed_user_pk)
        group_student_history.is_deleted = False
        group_student_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        group_student_history = self.get_group_status_ent(changed_user_pk)
        group_student_history.is_deleted = True
        group_student_history.save()
        super(GroupStatus, self).delete()

    def get_group_status_ent(self, user_pk):
        return GroupStatusHistory(origin_id=self.pk,
                                  changed_user_id=user_pk,
                                  description=self.description,
                                  is_active=self.is_active,
                                  created_date=self.created_date)


class GroupStatusHistory(models.Model):
    origin_id = models.IntegerField()
    title = models.CharField(max_length=120)
    changed_user_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class LessonGroupStudentStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super(LessonGroupStudentStatus, self).save(*args, **kwargs)
        lesson_group_student_status_history = self.get_lesson_group_student_status_ent()
        lesson_group_student_status_history.is_deleted = False
        lesson_group_student_status_history.save()

    def delete(self, *args):
        lesson_group_student_status_history = self.get_lesson_group_student_status_ent()
        lesson_group_student_status_history.is_deleted = True
        lesson_group_student_status_history.save()
        super(LessonGroupStudentStatus, self).delete()

    def get_lesson_group_student_status_ent(self, user_id=None):
        return LessonGroupStudentStatusHistory(origin_id=self.pk,
                                               user_id=user_id if user_id else self.user.pk,
                                               description=self.description,
                                               is_active=self.is_active,
                                               created_date=self.created_date)


class LessonGroupStudentStatusHistory(models.Model):
    origin_id = models.IntegerField()
    user_id = models.IntegerField()
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)
