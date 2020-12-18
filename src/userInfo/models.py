from django.db import models
from django.conf import settings
from portal.api.constants import ROLE_CHOICES
from portal.api.constants import GENDER_CHOICES
from .api.constants import CERTIFICATE_CHOICES, BLUE
from statuses.models import UserStatus
from django.core.validators import MaxValueValidator, MinValueValidator


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_role')
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user.username) + "  (" + self.role + ")"

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(UserRole, self).save(*args, **kwargs)
        user_role_history = self.get_user_role_ent(changed_user_pk)
        user_role_history.is_deleted = False
        user_role_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk')
        user_role_history = self.get_user_role_ent(changed_user_pk)
        user_role_history.is_deleted = True
        user_role_history.save()
        super(UserRole, self).delete()

    def get_user_role_ent(self, user_pk=None):
        return UserRoleHistory(origin_id=self.pk,
                               changed_user_id=user_pk,
                               user_id=self.user.pk,
                               role=self.role)


class UserRoleHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField()
    role = models.CharField(max_length=2)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_student')
    # status = models.ForeignKey(UserStatus, on_delete=models.PROTECT, null=True, blank=True)
    has_payment = models.BooleanField(default=True)
    has_contract = models.BooleanField(default=True)
    is_password_reset = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    grade = models.IntegerField()
    phone = models.BigIntegerField(validators=[MaxValueValidator(7999999999), MinValueValidator(7000000000)], null=True,blank=True)
    certificate = models.CharField(max_length=1, choices=CERTIFICATE_CHOICES, default=BLUE)
    dob = models.DateField(auto_now_add=False, auto_now=False)
    school = models.CharField(max_length=120)
    home_phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    target_subject = models.CharField(max_length=120, null=True, blank=True)
    target_from = models.CharField(max_length=120, null=True, blank=True)
    instagram = models.CharField(max_length=120, null=True, blank=True)
    force_access_until = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.user.last_name+' '+self.user.first_name

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(Student, self).save(*args, **kwargs)
        student_history = self.get_student_ent(changed_user_pk)
        student_history.is_deleted = False
        student_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk')
        student_history = self.get_student_ent(changed_user_pk)
        student_history.is_deleted = True
        student_history.save()
        super(Student, self).delete()

    def get_student_ent(self, user_pk=None):
        return StudentHistory(origin_id=self.pk,
                              user_id=self.user.pk,
                              changed_user_id=user_pk,
                              has_payment=self.has_payment,
                              has_contract=self.has_contract,
                              is_password_reset=self.is_password_reset,
                              gender=self.gender,
                              grade=self.grade,
                              phone=self.phone,
                              certificate=self.certificate,
                              dob=self.dob,
                              school=self.school,
                              home_phone=self.home_phone,
                              address=self.address,
                              target_subject=self.target_subject,
                              target_from=self.target_from,
                              instagram=self.instagram,
                              force_access_until=self.force_access_until,
                              created_date=self.created_date)


class StudentHistory(models.Model):
    origin_id = models.IntegerField()
    user_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    # status_id = models.IntegerField(null=True, blank=True)
    has_payment = models.BooleanField(default=True)
    has_contract = models.BooleanField(default=True)
    is_password_reset = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    grade = models.IntegerField()
    phone = models.BigIntegerField(validators=[MaxValueValidator(7999999999), MinValueValidator(7000000000)], null=True, blank=True)
    certificate = models.CharField(max_length=1, default=BLUE)
    dob = models.DateField(auto_now_add=False, auto_now=False)
    school = models.CharField(max_length=120)
    home_phone = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    target_subject = models.CharField(max_length=120, null=True, blank=True)
    target_from = models.CharField(max_length=120, null=True, blank=True)
    instagram = models.CharField(max_length=120, null=True, blank=True)
    force_access_until = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class Staff(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_staff')
    dob = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    is_password_reset = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return '{} {}'.format(self.user.last_name, self.user.first_name)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(Staff, self).save(*args, **kwargs)
        staff_history = self.get_staff_ent(changed_user_pk)
        staff_history.is_deleted = False
        staff_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        staff_history = self.get_staff_ent(changed_user_pk)
        staff_history.is_deleted = True
        staff_history.save()
        super(Staff, self).delete()

    def get_staff_ent(self, user_pk=None):
        return StaffHistory(origin_id=self.pk,
                            user_id=self.user.pk,
                            changed_user_id=user_pk,
                            dob=self.dob,
                            is_password_reset=self.is_password_reset,
                            created_date=self.created_date)


class StaffHistory(models.Model):
    origin_id = models.IntegerField()
    user_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    dob = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    is_password_reset = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class Parent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_parent')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='student_parent')
    is_main = models.BooleanField(default=False)
    phone = models.BigIntegerField(validators=[MaxValueValidator(7999999999), MinValueValidator(7000000000)], null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(Parent, self).save(*args, **kwargs)
        parent_history = self.get_parent_ent(changed_user_pk)
        parent_history.is_deleted = False
        parent_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        parent_history = self.get_parent_ent(changed_user_pk)
        parent_history.is_deleted = True
        parent_history.save()
        super(Parent, self).delete()

    def get_parent_ent(self, user_pk):
        return ParentHistory(origin_id=self.pk,
                             user_id=self.user.pk,
                             changed_user_id=user_pk if user_pk else 1,
                             student_id=self.student.pk,
                             phone=self.phone,
                             is_main=self.is_main,
                             created_date=self.created_date)


class ParentHistory(models.Model):
    origin_id = models.IntegerField()
    user_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    student_id = models.IntegerField()
    is_main = models.BooleanField(default=False)
    phone = models.BigIntegerField(validators=[MaxValueValidator(7999999999), MinValueValidator(7000000000)], null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class StudentFreeze(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="u_student_freeze")
    from_date = models.DateField()
    to_date = models.DateField()
    comment = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(StudentFreeze, self).save(*args, **kwargs)
        student_freeze_history_ent = self.get_student_freeze_history_ent(changed_user_pk)
        student_freeze_history_ent.is_deleted = False
        student_freeze_history_ent.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        student_freeze_history_ent = self.get_student_freeze_history_ent(changed_user_pk)
        student_freeze_history_ent.is_deleted = True
        student_freeze_history_ent.save()
        super(StudentFreeze, self).delete()

    def get_student_freeze_history_ent(self, user_id):
        return StudentFreezeHistory(origin_id=self.pk,
                                    changed_user_id=user_id,
                                    student_id=self.student.pk,
                                    from_date=self.from_date,
                                    to_date=self.to_date,
                                    comment=self.comment,
                                    created_date=self.created_date)


class StudentFreezeHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    student_id = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    comment = models.CharField(max_length=120)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_date']


class StudentGroupFreeze(models.Model):
    lesson_group_student = models.ForeignKey('groupsAndLessons.LessonGroupStudent', on_delete=models.PROTECT, related_name="lgs_student_group_freeze")
    date = models.DateField()
    comment = models.CharField(max_length=120)

    def save(self, *args, **kwargs):
        changed_user_id = kwargs.pop('user_pk', None)
        super(StudentGroupFreeze, self).save(*args, **kwargs)
        student_group_freeze_history_ent = self.get_student_group_freeze_history(changed_user_id)
        student_group_freeze_history_ent.is_deleted = False
        student_group_freeze_history_ent.save()

    def delete(self, *args, **kwargs):
        changed_user_id = kwargs.pop('user_pk', None)
        student_group_freeze_history_ent = self.get_student_group_freeze_history(changed_user_id)
        student_group_freeze_history_ent.is_deleted = True
        student_group_freeze_history_ent.save()
        super(StudentGroupFreeze, self).delete()

    def get_student_group_freeze_history(self, user_id):
        return StudentGroupFreezeHistory(origin_id=self.pk,
                                         changed_user_id=user_id,
                                         lesson_group_student_id=self.lesson_group_student.pk,
                                         date=self.date,
                                         comment=self.comment)


class StudentGroupFreezeHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    lesson_group_student_id = models.IntegerField()
    date = models.DateField()
    comment = models.CharField(max_length=120)
    updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']
