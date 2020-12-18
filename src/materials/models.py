from django.db import models
from django.conf import settings


class Subject(models.Model):
    title = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(Subject, self).save(*args, **kwargs)
        subject_history = self.get_subject_ent(changed_user_pk)
        subject_history.is_deleted = False
        subject_history.save()
        return self

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        subject_history = self.get_subject_ent(changed_user_pk)
        subject_history.is_deleted = True
        subject_history.save()
        super(Subject, self).delete()

    def get_subject_ent(self, user_pk):
        return SubjectHistory(origin_id=self.pk,
                              created_user_id=user_pk if user_pk else 1,
                              title=self.title,
                              created_date=self.created_date)


class SubjectHistory(models.Model):
    origin_id = models.IntegerField()
    created_user_id = models.IntegerField()
    title = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, null=True, blank=True, related_name='topic')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='topics')
    title = models.CharField(max_length=120)
    is_endpoint = models.BooleanField(default=False)
    is_mid_control = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        subject_title = self.subject.title if self.subject is not None else None
        return '{} {}'.format(self.title, subject_title)

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(Topic, self).save(*args, **kwargs)
        topic_history = self.get_topic_ent(changed_user_pk)
        topic_history.is_deleted = False
        topic_history.save()
        return self

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        topic_history = self.get_topic_ent(changed_user_pk)
        topic_history.is_deleted = True
        topic_history.save()
        super(Topic, self).delete()

    def get_topic_ent(self, user_pk):
        return TopicHistory(origin_id=self.pk,
                            created_user_id=user_pk if user_pk else 1,
                            subject_id=self.subject.pk if self.subject else None,
                            parent_id=self.parent.pk if self.parent else None,
                            title=self.title,
                            is_endpoint=self.is_endpoint,
                            is_mid_control=self.is_mid_control,
                            order=self.order,
                            created_date=self.created_date)


class TopicHistory(models.Model):
    origin_id = models.IntegerField()
    created_user_id = models.IntegerField()
    subject_id = models.IntegerField(null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=120)
    is_endpoint = models.BooleanField(default=False)
    is_mid_control = models.BooleanField(default=False)
    order = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class Video(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='t_video')
    title = models.CharField(max_length=120, null=True, blank=True)
    duration = models.BigIntegerField()
    link = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['topic', 'title']

    def __str__(self):
        return self.topic.title

    def save(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        super(Video, self).save(*args, **kwargs)
        video_history = self.get_video_ent(changed_user_pk)
        video_history.is_deleted = False
        video_history.save()
        return self

    def delete(self, *args, **kwargs):
        changed_user_pk = kwargs.pop('user_pk', None)
        video_history = self.get_video_ent(changed_user_pk)
        video_history.is_deleted = True
        video_history.save()
        super(Video, self).delete()

    def get_video_ent(self, user_pk):
        return VideoHistory(origin_id=self.pk,
                            created_user_id=user_pk,
                            topic_id=self.topic.pk,
                            title=self.title,
                            duration=self.duration,
                            link=self.link,
                            created_date=self.created_date)


class VideoHistory(models.Model):
    origin_id = models.IntegerField()
    created_user_id = models.IntegerField(null=True, blank=True)
    topic_id = models.IntegerField()
    title = models.CharField(max_length=120, null=True, blank=True)
    duration = models.BigIntegerField()
    link = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class TopicTest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    title = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['topic', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(TopicTest, self).save(*args, **kwargs)
        topic_test_history = self.get_topic_test_ent()
        topic_test_history.is_deleted = False
        topic_test_history.save()

    def delete(self, *args):
        topic_test_history = self.get_topic_test_ent()
        topic_test_history.is_deleted = True
        topic_test_history.save()
        super(TopicTest, self).delete()

    def get_topic_test_ent(self, user_id=None):
        return TopicTestHistory(origin_id=self.pk,
                                user_id=user_id if user_id else self.user.pk,
                                topic_id=self.topic.pk,
                                title=self.title,
                                created_date=self.created_date)


class TopicTestHistory(models.Model):
    origin_id = models.IntegerField()
    user_id = models.IntegerField()
    topic_id = models.IntegerField()
    title = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return str(self.origin_id)


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    topic_test = models.ForeignKey(TopicTest, on_delete=models.PROTECT)
    text = models.TextField()
    image = models.ImageField(upload_to=settings.IMG_PATH['QUESTION'],
                              null=True,
                              blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['topic_test']

    def __str__(self):
        return self.topic_test.title

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, *kwargs)
        question_history = self.get_question_ent()
        question_history.is_deleted = False
        question_history.save()

    def delete(self, *args):
        question_history = self.get_question_ent()
        question_history.is_deleted = True
        question_history.save()
        super(Question, self).delete()

    def get_question_ent(self, user_id=None):
        return QuestionHistory(origin_id=self.pk,
                               user_id=user_id if user_id else self.user.pk,
                               topic_test_id=self.topic_test.pk,
                               text=self.text,
                               image=self.image)


class QuestionHistory(models.Model):
    origin_id = models.IntegerField()
    user_id = models.IntegerField()
    topic_test_id = models.IntegerField()
    text = models.TextField()
    image = models.ImageField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    uploaded_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return str(self.origin_id)


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    text = models.TextField()
    image = models.ImageField(upload_to=settings.IMG_PATH['ANSWER'],
                              null=True,
                              blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['question']

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(Answer, self).save(*args, **kwargs)
        answer_history = self.get_answer_ent()
        answer_history.is_deleted = False
        answer_history.save()

    def delete(self, *args):
        answer_history = self.get_answer_ent()
        answer_history.is_deleted = True
        answer_history.save()
        super(Answer, self).delete()

    def get_answer_ent(self, user_id=None):
        return AnswerHistory(origin_id=self.pk,
                             user_id=user_id if user_id else self.user.pk,
                             question=self.question.id,
                             text=self.text,
                             image=self.image,
                             created_date=self.created_date)


class AnswerHistory(models.Model):
    origin_id = models.IntegerField()
    user_id = models.IntegerField()
    question = models.IntegerField()
    text = models.TextField()
    image = models.ImageField()
    created_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    uploaded_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return str(self.origin_id)
