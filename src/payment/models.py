from django.db import models
from django.contrib.postgres.fields import JSONField
from userInfo.models import Staff


class PreTeacherSalary(models.Model):
    infos = JSONField()
    salary_for = models.DateField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(PreTeacherSalary, self).save(*args, **kwargs)
        pre_teacher_salary_history = self.get_pre_teacher_salary_history_ent(changed_user_pk)
        pre_teacher_salary_history.is_deleted = False
        pre_teacher_salary_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        pre_teacher_salary_history = self.get_pre_teacher_salary_history_ent(changed_user_pk)
        pre_teacher_salary_history.is_deleted = True
        pre_teacher_salary_history.save()
        super(PreTeacherSalary, self).delete()

    def get_pre_teacher_salary_history_ent(self, user_id):
        return PreTeacherSalaryHistory(origin_id=self.pk,
                                       changed_user_id=user_id,
                                       infos=self.infos,
                                       salary_for=self.salary_for,
                                       created_date=self.created_date)


class PreTeacherSalaryHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    infos = JSONField()
    salary_for = models.DateField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']


class PostTeacherSalary(models.Model):
    infos = JSONField()
    salary_for = models.DateField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(PostTeacherSalary, self).save(*args, **kwargs)
        post_teacher_salary_history = self.get_post_teacher_salary_history_ent(changed_user_pk)
        post_teacher_salary_history.is_deleted = False
        post_teacher_salary_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        post_teacher_salary_history = self.get_post_teacher_salary_history_ent(changed_user_pk)
        post_teacher_salary_history.is_deleted = True
        post_teacher_salary_history.save()
        super(PostTeacherSalary, self).delete()

    def get_post_teacher_salary_history_ent(self, user_id):
        return PostTeacherSalaryHistory(origin_id=self.pk,
                                        changed_user_id=user_id,
                                        infos=self.infos,
                                        salary_for=self.salary_for,
                                        created_date=self.created_date)


class PostTeacherSalaryHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    infos = JSONField()
    salary_for = models.DateField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']


class TeacherSalaryFile(models.Model):
    post_teacher_salary = models.ForeignKey(PostTeacherSalary, on_delete=models.DO_NOTHING)
    link = models.TextField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)


class TeacherSalaryCategoryLevel(models.Model):
    category = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(TeacherSalaryCategoryLevel, self).save(*args, **kwargs)
        teacher_salary_category_level = self.get_teacher_salary_category_level_history_ent(changed_user_pk)
        teacher_salary_category_level.is_deleted = False
        teacher_salary_category_level.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        teacher_salary_category_level = self.get_teacher_salary_category_level_history_ent(changed_user_pk)
        teacher_salary_category_level.is_deleted = True
        teacher_salary_category_level.save()
        super(TeacherSalaryCategoryLevel, self).delete()

    def get_teacher_salary_category_level_history_ent(self, user_id):
        return TeacherSalaryCategoryLevelHistory(origin_id=self.pk,
                                                 changed_user_id=user_id,
                                                 category=self.category,
                                                 created_date=self.created_date)


class TeacherSalaryCategoryLevelHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=120)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']


class TeacherSalaryCategory(models.Model):
    teacher_salary_category_level = models.ForeignKey(TeacherSalaryCategoryLevel, on_delete=models.PROTECT)
    lessons_per_week = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '{} Аптасына {} рет'.format(self.teacher_salary_category_level.category, str(self.lessons_per_week))
    
    class Meta:
        unique_together = ('teacher_salary_category_level', 'lessons_per_week')

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(TeacherSalaryCategory, self).save(*args, **kwargs)
        teacher_salary_category_history = self.get_teacher_salary_category_history_ent(changed_user_pk)
        teacher_salary_category_history.is_deleted = False
        teacher_salary_category_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        teacher_salary_category_history = self.get_teacher_salary_category_history_ent(changed_user_pk)
        teacher_salary_category_history.is_deleted = True
        teacher_salary_category_history.save()
        super(TeacherSalaryCategory, self).delete()

    def get_teacher_salary_category_history_ent(self, user_id):
        return TeacherSalaryCategoryHistory(origin_id=self.pk,
                                            changed_user_id=user_id,
                                            teacher_salary_category_level_id=self.teacher_salary_category_level.pk,
                                            lessons_per_week=self.lessons_per_week,
                                            created_date=self.created_date)


class TeacherSalaryCategoryHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    teacher_salary_category_level_id = models.IntegerField()
    lessons_per_week = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']


class TeacherSalaryCoefficient(models.Model):
    teacher_salary_category = models.ForeignKey(TeacherSalaryCategory, on_delete=models.CASCADE)
    coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(TeacherSalaryCoefficient, self).save(*args, **kwargs)
        teacher_salary_coefficient_history = self.get_teacher_salary_coefficient_history_ent(changed_user_pk)
        teacher_salary_coefficient_history.is_deleted = False
        teacher_salary_coefficient_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        teacher_salary_coefficient_history = self.get_teacher_salary_coefficient_history_ent(changed_user_pk)
        teacher_salary_coefficient_history.is_deleted = True
        teacher_salary_coefficient_history.save()
        super(TeacherSalaryCoefficient, self).delete()

    def get_teacher_salary_coefficient_history_ent(self, user_id):
        return TeacherSalaryCoefficientHistory(origin_id=self.pk,
                                               changed_user_id=user_id,
                                               teacher_salary_category_id=self.teacher_salary_category.pk,
                                               coefficient=self.coefficient,
                                               price=self.price)


class TeacherSalaryCoefficientHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    teacher_salary_category_id = models.IntegerField()
    coefficient = models.DecimalField(max_digits=2, decimal_places=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']


class TeacherCategory(models.Model):
    teacher_salary_category_level = models.ForeignKey(TeacherSalaryCategoryLevel, on_delete=models.PROTECT)
    teacher = models.OneToOneField(Staff, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(TeacherCategory, self).save(*args, **kwargs)
        teacher_category_history = self.get_teacher_category_history_ent(changed_user_pk)
        teacher_category_history.is_deleted = False
        teacher_category_history.save()

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        teacher_category_history = self.get_teacher_category_history_ent(changed_user_pk)
        teacher_category_history.is_deleted = True
        teacher_category_history.save()
        super(TeacherCategory, self).delete()

    def get_teacher_category_history_ent(self, user_id):
        return TeacherCategoryHistory(origin_id=self.pk,
                                      changed_user_id=user_id,
                                      teacher_salary_category_level_id=self.teacher_salary_category_level.pk,
                                      teacher_id=self.teacher.pk,
                                      created_date=self.created_date)


class TeacherCategoryHistory(models.Model):
    origin_id = models.IntegerField()
    changed_user_id = models.IntegerField(null=True, blank=True)
    teacher_salary_category_level_id = models.IntegerField()
    teacher_id = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-updated_date']
