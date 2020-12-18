from rest_framework import serializers
from groupsAndLessons.models import LessonGroupStudent, TopicPlan, StudentPlan
from portal.api.serializer import UserShortSerializer
from ..models import GroupStudentVisit, StudentVisit, TopicQuizMark, TrialTest, TrialTestMark, LessonVideoAction
from materials.api.serializers import TopicSerializer
import datetime
from django.db.models import Q


class LessonGroupStudentsABSSerializer(serializers.ModelSerializer):

    user_info = serializers.SerializerMethodField(read_only=True)
    student_visit = serializers.SerializerMethodField()
    has_student_freeze = serializers.SerializerMethodField()

    @staticmethod
    def get_user_info(instance):
        try:
            return UserShortSerializer(instance.student_plan.student).data
        except AttributeError:
            return None

    def get_student_visit(self, lesson_group_student):
        return None
        # try:
        #     abs_date = self.context.get('abs_date', None)
        #     print('abs_date', abs_date)
        #     if abs_date is None:
        #         return None
        #     try:
        #         student_visit = lesson_group_student.lgs_student_visit.get(group_student_visit__abs_date=abs_date)
        #         print('student_visit', student_visit)
        #         return StudentVisitSerializer(student_visit).data
        #     except StudentVisit.DoesNotExist:
        #         return None
        # except AttributeError as e:
        #     print('error', e)
        #     return None

    def get_has_student_freeze(self, lesson_group_student):
        try:
            abs_date = self.context.get('abs_date', None)
            if abs_date is None:
                return False
            student = lesson_group_student.student_plan.student
            student_freeze = student.u_student_freeze.filter(Q(from_date__lte=abs_date)
                                                             & Q(to_date__gte=abs_date))
            student_group_freeze = lesson_group_student.lgs_student_group_freeze.filter(date=abs_date)
            if student_freeze.count() != 0 or student_group_freeze.count() != 0:
                return True
            return False
        except AttributeError:
            return None

    class Meta:
        model = LessonGroupStudent
        fields = (
            'pk',
            'student_plan',
            'lesson_group',
            'started_date',
            'student_visit',
            'has_student_freeze',
            'user_info'
        )
        read_only_fields = ('pk', 'started_date', 'student_plan', 'lesson_group')


class LessonGroupStudentsABSEditSerializer(serializers.ModelSerializer):

    user_info = serializers.SerializerMethodField(read_only=True)
    student_visit = serializers.SerializerMethodField()
    has_student_freeze = serializers.SerializerMethodField()

    @staticmethod
    def get_user_info(instance):
        try:
            return UserShortSerializer(instance.student_plan.student).data
        except AttributeError:
            return None

    @staticmethod
    def get_student_visit(instance):
        try:
            group_student_visit = instance.lesson_group.lg_group_student_visit.all().order_by('-abs_date').first()
            student_visit_serializer = StudentVisitSerializer(group_student_visit.group_student_visit.get(lesson_group_student=instance)).data
            return student_visit_serializer
        except AttributeError:
            return None
        except StudentVisit.DoesNotExist:
            return None

    def get_has_student_freeze(self, lesson_group_student):
        try:
            abs_date = self.context.get('abs_date', None)
            if abs_date is None:
                return False
            student = lesson_group_student.student_plan.student
            student_freeze = student.u_student_freeze.filter(Q(from_date__lte=abs_date)
                                                             & Q(to_date__gte=abs_date))
            student_group_freeze = lesson_group_student.lgs_student_group_freeze.filter(date=abs_date)
            if student_freeze.count() != 0 or student_group_freeze.count() != 0:
                return True
            return False
        except AttributeError:
            return None

    class Meta:
        model = LessonGroupStudent
        fields = (
            'pk',
            'student_plan',
            'lesson_group',
            'started_date',
            'student_visit',
            'has_student_freeze',
            'user_info'
        )
        read_only_fields = ('pk', 'started_date', 'student_plan', 'lesson_group')


class GroupStudentVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupStudentVisit
        fields = (
            'pk',
            'lesson_group',
            'abs_date',
            'created_date',
        )
        read_only_fields = ('pk', 'created_date',)

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        group_student_visit = GroupStudentVisit(**validated_data)
        group_student_visit.save(user_pk=user_pk)
        return group_student_visit


class StudentVisitSerializer(serializers.ModelSerializer):

    user_info = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_user_info(instance):
        try:
            student_user = instance.lesson_group_student.student_plan.student
            return UserShortSerializer(student_user).data
        except AttributeError:
            return None

    class Meta:
        model = StudentVisit
        fields = (
            'pk',
            'group_student_visit',
            'lesson_group_student',
            'attendance',
            'home_work',
            'no_home_work',
            'user_info',
        )
        read_only_fields = ('pk',)
        extra_kwargs = {'group_student_visit': {'allow_null': True}}

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        student_visit = StudentVisit(**validated_data)
        group_student_visit = student_visit.group_student_visit
        student = student_visit.lesson_group_student.student_plan.student
        student_freeze = student.u_student_freeze.filter(Q(from_date__lte=group_student_visit.abs_date)
                                                         & Q(to_date__gte=group_student_visit.abs_date))
        student_group_freeze = validated_data.get('lesson_group_student').lgs_student_group_freeze.filter(date=group_student_visit.abs_date)
        if student_freeze.count() == 0 and student_group_freeze.count() == 0:
            student_visit.no_home_work = True if not student_visit.attendance else student_visit.no_home_work
            student_visit.home_work = 0.0 if not student_visit.attendance or student_visit.no_home_work else student_visit.home_work
            student_visit.save(user_pk=user_pk)
        return student_visit

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        group_student_visit = instance.group_student_visit
        student = instance.lesson_group_student.student_plan.student
        student_freeze = student.u_student_freeze.filter(Q(from_date__lte=group_student_visit.abs_date)
                                                         & Q(to_date__gte=group_student_visit.abs_date))
        student_group_freeze = validated_data.get('lesson_group_student').lgs_student_group_freeze.filter(date=group_student_visit.abs_date)
        if student_freeze.count() == 0 and student_group_freeze.count() == 0:
            has_changes = False
            for attr, value in validated_data.items():
                if getattr(instance, attr) != value:
                    has_changes = True
                    setattr(instance, attr, value)
            if has_changes:
                instance.no_home_work = True if not instance.attendance else instance.no_home_work
                instance.home_work = 0.0 if not instance.attendance or instance.no_home_work else instance.home_work
                instance.save(user_pk=user_pk)
        return instance


class GroupWithStudentVisitSerializer(serializers.ModelSerializer):

    student_visit = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_student_visit(instance):
        try:
            student_visits = instance.group_student_visit.all()\
                .order_by('lesson_group_student__student_plan__student__pk')
            return StudentVisitSerializer(student_visits, many=True).data
        except AttributeError:
            return None

    class Meta:
        model = GroupStudentVisit
        fields = (
            'pk',
            'lesson_group',
            'abs_date',
            'created_date',
            'student_visit',
        )
        read_only_fields = ('pk', 'created_date',)


class TopicQuizMarkSerializer(serializers.ModelSerializer):

    can_edit = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_can_edit(instance):
        try:
            subject_plan = TopicPlan.objects.get(pk=instance.topic_plan.pk).subject_plan
            student_plan = subject_plan.student_plan
            lesson_group_student = LessonGroupStudent.objects.filter(student_plan=student_plan)
            for ent in lesson_group_student:
                lesson_group = ent.lesson_group
                group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group=lesson_group)
                                                                       & Q(abs_date__gt=instance.created_date)
                                                                       & Q(group_student_visit__attendance=True))
                if len(group_student_visit) != 0:
                    return False
            return True
        except AttributeError:
            return False

    class Meta:
        model = TopicQuizMark
        fields = (
            'pk',
            'topic_plan',
            'practice',
            'theory',
            'can_edit',
            'created_date',
        )

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        topic_quiz_mark = TopicQuizMark(**validated_data)
        topic_quiz_mark.save(user_pk=user_pk)
        return topic_quiz_mark

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        has_changes = False
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                has_changes = True
                setattr(instance, attr, value)
        if has_changes:
            instance.save(user_pk=user_pk)
        return instance


class TopicQuizByTopicPlanListSerializer(serializers.ModelSerializer):

    topic_info = serializers.SerializerMethodField(read_only=True)
    topic_quiz = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_topic_info(instance):
        try:
            return TopicSerializer(instance.topic).data
        except AttributeError:
            return None

    @staticmethod
    def get_topic_quiz(instance):
        try:
            result = []
            result += TopicQuizMarkSerializer(instance.tqm_topic_plan.all().order_by('created_date'), many=True).data
            if len(result) == 0 or (not result[-1]['can_edit'] and len(result) == 1 and (
                    (result[0]['theory'] is None or result[0]['theory'] < 70) and (
                    result[0]['practice'] is None or result[0]['practice'] < 70))):
                result.append(TopicQuizMarkSerializer(None).data)
            return result
        except AttributeError:
            return None

    class Meta:
        model = TopicPlan
        fields = (
            'pk',
            'subject_plan',
            'topic',
            'topic_info',
            'topic_quiz',
            'created_date'
        )


class TrialTestMarkSerializer(serializers.ModelSerializer):

    can_edit = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_can_edit(instance):
        try:
            student_plan = StudentPlan.objects.get(Q(student=instance.trial_test.student)
                                                   & Q(subject_plan__subject=instance.trial_test.subject))
            # student_plan = StudentPlan.objects.filter(student=instance.trial_test.student)
            lesson_group_student = LessonGroupStudent.objects.filter(student_plan=student_plan)
            for ent in lesson_group_student:
                lesson_group = ent.lesson_group
                group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group=lesson_group)
                                                                       & Q(abs_date__gt=instance.created_date)
                                                                       & Q(group_student_visit__attendance=True))
                if len(group_student_visit) != 0:
                    return False
            return True
        except AttributeError:
            return False
        except StudentPlan.DoesNotExist:
            return False

    class Meta:
        model = TrialTestMark
        fields = (
            'pk',
            'trial_test',
            'mark',
            'date',
            'can_edit',
            'created_date',
        )

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        trial_test_mark = TrialTestMark(**validated_data)
        trial_test_mark.save(user_pk=user_pk)
        return trial_test_mark

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        has_changes = False
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                has_changes = True
                setattr(instance, attr, value)
        if has_changes:
            instance.save(user_pk=user_pk)
        return instance


class TrialTestSerializer(serializers.ModelSerializer):

    trial_test_marks = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_trial_test_marks(instance):
        try:
            trial_test_marks = instance.ttm_trial_test.all().order_by('-date')
            result = []
            result += TrialTestMarkSerializer(trial_test_marks, many=True).data
            if len(result) == 0 or not result[-1]['can_edit']:
                result.append(TrialTestMarkSerializer(None).data)
            return result
        except AttributeError:
            return None

    class Meta:
        model = TrialTest
        fields = (
            'pk',
            'student',
            'subject',
            'trial_test_marks'
        )


class LessonVideoActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonVideoAction
        fields = (
            'pk',
            'lesson_group_student',
            'topic',
            'created_date'
        )
