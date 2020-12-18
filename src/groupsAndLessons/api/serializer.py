from rest_framework import serializers
from ..models import (
    StudentPlan,
    SubjectPlan,
    TopicPlan,
    Office,
    Schedule,
    LessonGroup,
    LessonGroupSchedule,
    LessonGroupStudent,
    GroupReplacement,
    LessonGroupStudentShortSchedule,
    DayOff,
    GroupTimeTransfer,
    GroupSchedule,
)
from portal.api.serializer import UserSerializer, UserShortSerializer
from materials.api.serializers import SubjectSerializer
from .utils import recalculate_student_plan_progress_by_student_plan
from portal.api.constants import WEEK_DAY_CHOICES, WEEK_DAY_SHORT_NAME


class FilteredTopicPlanSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        is_mid_control = self.context.pop('is_mid_control', None)
        if is_mid_control is not None:
            data = data.filter(topic__is_mid_control=is_mid_control)
        else:
            data = data.all()
        return super(FilteredTopicPlanSerializer, self).to_representation(data)


class TopicPlanSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredTopicPlanSerializer
        model = TopicPlan
        fields = (
            'pk',
            'subject_plan',
            'topic',
            'tutorial',
            'class_work',
            'home_work',
            'created_date'
        )
        read_only_field = ('pk', 'subject_plan', 'created_date')
        extra_kwargs = {'subject_plan': {'required': False}}


class SubjectPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectPlan
        fields = (
            'pk',
            'subject',
            'created_date'
        )
        read_only_field = ('pk', 'created_date')


class SubjectTopicPlanSerializer(serializers.ModelSerializer):

    topic_plan = TopicPlanSerializer(many=True)


    class Meta:
        model = SubjectPlan
        fields = (
            'pk',
            'subject',
            'topic_plan',
            'created_date'
        )
        read_only_fields = ('topic_plan', 'created_date')


class StudentSubjectTopicSerializer(serializers.ModelSerializer):
    subject_plan = SubjectTopicPlanSerializer(many=True)
    subject_info = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_subject_info(instance):
        try:
            return SubjectSerializer(instance.subject).data
        except AttributeError:
            return None

    class Meta:
        model = StudentPlan
        fields = (
            'pk',
            'student',
            'subject',
            'progress',
            'created_date',
            'subject_plan',
            'subject_info'
        )
        read_only_fields = ('pk', 'progress', 'created_date')

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        sj_plans = validated_data.pop('subject_plan', None)
        student_plan = StudentPlan(**validated_data)
        student_plan.save(user_pk=user_pk)
        if sj_plans:
            for sj_plan in sj_plans:
                t_plans = sj_plan.pop('topic_plan', None)
                subject_plan = self.save_subject_plan(student_plan, user_pk, **sj_plan)
                if t_plans:
                    for t_plan in t_plans:
                        topic_plan = self.save_topic_plan(subject_plan, user_pk, **t_plan)
        recalculate_student_plan_progress_by_student_plan(student_plan, user_pk)
        return student_plan

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        sj_plans = validated_data.pop('subject_plan', None)
        student_plan = instance
        subjects = []
        topic = []
        subject_plans = []
        topic_plans = []
        if sj_plans:
            for sj_plan in sj_plans:
                t_plans = sj_plan.pop('topic_plan', None)
                subjects.append(sj_plan['subject'])
                if not SubjectPlan.objects.filter(student_plan=student_plan, subject=sj_plan['subject']).exists():
                    subject_plan = self.save_subject_plan(student_plan, user_pk, **sj_plan)
                    subject_plans.append(subject_plan)
                else:
                    subject_plan = student_plan.subject_plan.get(subject=sj_plan['subject'])
                    subject_plans.append(subject_plan)

                if t_plans:
                    for t_plan in t_plans:
                        topic.append(t_plan['topic'])
                        if not TopicPlan.objects.filter(topic=t_plan['topic'],
                                                        subject_plan__student_plan=student_plan).exists():
                            topic_plan = self.save_topic_plan(subject_plan, user_pk, **t_plan)
                            topic_plans.append(topic_plan)
                        else:
                            topic_plan = student_plan\
                                            .subject_plan.get(subject=sj_plan['subject'])\
                                            .topic_plan.get(topic=t_plan['topic'])
                            topic_plans.append(topic_plan)
        self.remove_not_listed_topic_plans(student_plan, topic_plans, user_pk)
        self.remove_not_listed_subject_plans(student_plan, subject_plans, user_pk)
        recalculate_student_plan_progress_by_student_plan(student_plan, user_pk)
        return student_plan

    @staticmethod
    def save_subject_plan(student_plan, user_pk, **sj_plan):
        subject_plan = SubjectPlan.objects.create(student_plan=student_plan, **sj_plan)
        subject_plan.save(user_pk=user_pk)
        return subject_plan

    @staticmethod
    def save_topic_plan(subject_plan, user_pk, **t_plan):
        topic_plan = TopicPlan.objects.create(subject_plan=subject_plan, **t_plan)
        topic_plan.save(user_pk=user_pk)
        return topic_plan

    @staticmethod
    def remove_not_listed_topic_plans(student_plan, topic_plans, user_pk):
        unnecessary_topic_plans = TopicPlan.objects.filter(subject_plan__student_plan=student_plan)\
                                .exclude(pk__in=[topic_plan.pk for topic_plan in topic_plans])
        for topic_plan in unnecessary_topic_plans:
            topic_plan.delete(user_pk=user_pk)

    @staticmethod
    def remove_not_listed_subject_plans(student_plan, subject_plans, user_pk):
        unnecessary_subject_plans = SubjectPlan.objects.filter(student_plan=student_plan)\
                                    .exclude(pk__in=[subject_plan.pk for subject_plan in subject_plans])
        for subject_plan in unnecessary_subject_plans:
            subject_plan.delete(user_pk=user_pk)


class OfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Office
        fields = (
            'pk',
            'title',
            'created_date'
        )
        read_only_fields = ('pk', 'created_date')

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        office = Office(**validated_data)
        office.save(user_pk=user_pk)
        return office


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = (
            'pk',
            'office',
            'week_num',
            'start_time',
            'finish_time',
            'created_date'
        )
        read_only_fields = ('pk', 'office', 'created_date')

    def to_representation(self, instance):
        data = super(ScheduleSerializer, self).to_representation(instance)
        if instance.office:
            data['office_info'] = {
                'title': instance.office.title
            }
        if instance.week_num:
            week_days = dict(WEEK_DAY_CHOICES)
            week_days_short_name = dict(WEEK_DAY_SHORT_NAME)
            data['week_day_info'] = {
                'week_day': instance.week_num,
                'title': week_days[instance.week_num],
                'short_title': week_days_short_name[instance.week_num],
            }
        data['group'] = None
        return data


class LessonGroupStudentSerializer(serializers.ModelSerializer):

    student = serializers.SerializerMethodField(read_only=True)
    lesson_group_student_short_schedule = serializers.SerializerMethodField(read_only=True)
    user_info = serializers.SerializerMethodField(read_only=True);

    @staticmethod
    def get_student(lesson_group_student):
        try:
            return lesson_group_student.student_plan.student.pk
        except AttributeError:
            return None

    @staticmethod
    def get_lesson_group_student_short_schedule(instance):
        try:
            lesson_group_student_short_schedule = instance.short_schedule.all()
            result = []
            for ent in lesson_group_student_short_schedule:
                result.append(LessonGroupStudentShortScheduleSerializer(ent).data)
            return result
        except AttributeError:
            return []

    @staticmethod
    def get_user_info(instance):
        try:
            return UserShortSerializer(instance.student_plan.student).data
        except AttributeError:
            return None

    class Meta:
        model = LessonGroupStudent
        fields = (
            'pk',
            'student_plan',
            'lesson_group',
            'started_date',
            'student',
            'lesson_group_student_short_schedule',
            'user_info',
            'created_date'
        )
        read_only_fields = ('pk', 'created_date')

    def to_representation(self, instance):
        data = super(LessonGroupStudentSerializer, self).to_representation(instance)
        data['started_date'] = instance.started_date.strftime('%Y-%m-%d')
        return data

    def create(self, validated_date):
        user_pk = validated_date.pop('user_pk')
        lesson_group_student = LessonGroupStudent(**validated_date)
        lesson_group_student.save(user_pk=user_pk)
        return lesson_group_student

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


class LessonGroupStudentShortScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonGroupStudentShortSchedule
        fields = (
            'pk',
            'lesson_group_student',
            'week_day_sign',
            'created_date'
        )
        read_only_fields = ('pk', 'created_date')
        extra_kwargs = {'lesson_group_student': {'allow_null':True, 'required': False}}

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        lesson_group_student = validated_data.pop('lesson_group_student')
        lesson_group_student_short_schedule = LessonGroupStudentShortSchedule(**validated_data)
        lesson_group_student_short_schedule.lesson_group_student = lesson_group_student
        lesson_group_student_short_schedule.save(user_pk=user_pk)
        return lesson_group_student_short_schedule


class LessonGroupWithScheduleSerializers(serializers.ModelSerializer):

    schedules = serializers.SerializerMethodField()
    plans = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    @staticmethod
    def get_schedules(lesson_group):
        try:
            group_schedule = GroupSchedule.objects.get(lesson_group=lesson_group)
            lesson_group_schedules = LessonGroupSchedule.objects.filter(group_schedule=group_schedule)
            schedule_list = []
            for ent in lesson_group_schedules:
                schedule_list.append(ScheduleSerializer(ent.schedule).data)
            return schedule_list
        except AttributeError:
            return None
        except GroupSchedule.DoesNotExist:
            return None

    @staticmethod
    def get_plans(lesson_group):
        try:
            lesson_group_student_plans = lesson_group.lesson_group_plan.all()
            student_plans = []
            for ent in lesson_group_student_plans:
                student_plans.append(LessonGroupStudentSerializer(ent).data)
            return student_plans
        except AttributeError:
            return None

    @staticmethod
    def get_student_count(lesson_group):
        try:
            student_count = lesson_group.lesson_group_plan.count()
            return student_count
        except AttributeError:
            return None

    class Meta:
        model = LessonGroup
        fields = (
            'pk',
            'teacher',
            'title',
            'student_limit',
            'send_message_on_no_payment',
            'schedules',
            'created_date',
            'plans',
            'student_count',
        )
        read_only_fields = ('pk', 'send_message_on_no_payment', 'schedules', 'created_date', 'plans', 'student_count')

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        lesson_group = LessonGroup(**validated_data)
        lesson_group.save(user_pk=user_pk)
        return lesson_group

    def to_representation(self, instance):
        data = super(LessonGroupWithScheduleSerializers, self).to_representation(instance)
        if instance.teacher:
            data['user_info'] = {
                'pk': instance.teacher.pk,
                'last_name': instance.teacher.last_name,
                'first_name': instance.teacher.first_name
            }
        return data

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


class LessonGroupStudentFullSerializer(serializers.ModelSerializer):

    user_info = serializers.SerializerMethodField(read_only=True)
    progress = serializers.SerializerMethodField(read_only=True)
    subject_info = serializers.SerializerMethodField(read_only=True)
    is_password_reset = serializers.SerializerMethodField(read_only=True)
    # plan_subjects = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_user_info(instance):
        try:
            user = instance.student_plan.student
            return UserShortSerializer(user).data
        except AttributeError:
            return None

    @staticmethod
    def get_progress(instance):
        try:
            return instance.student_plan.progress
        except AttributeError:
            return None

    @staticmethod
    def get_subject_info(instance):
        try:
            subject = instance.student_plan.subject
            return SubjectSerializer(subject).data
        except AttributeError:
            return None

    @staticmethod
    def get_is_password_reset(instance):
        try:
            return instance.student_plan.student.user_student.get().is_password_reset
        except AttributeError:
            return None

    # @staticmethod
    # def get_plan_subjects(instance):
    #     try:
    #         plan_subjects = instance.student_plan.subject_plan.all()
    #         subjects = []
    #         for ent in plan_subjects:
    #             subjects.append(SubjectSerializer(ent.subject).data)
    #         return subjects
    #     except AttributeError:
    #         return None

    class Meta:
        model = LessonGroupStudent
        fields = (
            'pk',
            'student_plan',
            'lesson_group',
            'started_date',
            'progress',
            'user_info',
            'subject_info',
            'is_password_reset',
            'created_date',
        )
        read_only_fields = ('pk', 'created_date')

    def to_representation(self, instance):
        data = super(LessonGroupStudentFullSerializer, self).to_representation(instance)
        student_subject_plan = instance.student_plan.subject_plan.all()
        if student_subject_plan.exists():
            data['plan_subjects'] = []
            for ent in student_subject_plan:
                tmp = {
                    'subject_info': SubjectSerializer(ent.subject).data,
                    'subject_plan': ent.pk
                }
                data['plan_subjects'].append(tmp)
        return data
# def to_representation(self, instance):
#     data = super(UserStaffSerializer, self).to_representation(instance)
#     result = {
#         'staff': data.pop('staff'),
#         'user': data,
#     }
#     return result



class LessonGroupFullSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField()
    student_plans = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    @staticmethod
    def get_schedules(lesson_group):
        try:
            group_schedule = GroupSchedule.objects.get(lesson_group=lesson_group)
            lesson_group_schedules = LessonGroupSchedule.objects.filter(group_schedule=group_schedule)
            schedule_list = []
            for ent in lesson_group_schedules:
                schedule_list.append(ScheduleSerializer(ent.schedule).data)
            return schedule_list
        except AttributeError:
            return None

    @staticmethod
    def get_student_plans(lesson_group):
        try:
            lesson_group_student_plans = lesson_group.lesson_group_plan.all().order_by(
                'student_plan__student__last_name', 'student_plan__student__first_name')
            student_plans = []
            for ent in lesson_group_student_plans:
                student_plans.append(LessonGroupStudentFullSerializer(ent).data)
            return student_plans
        except AttributeError:
            return None

    @staticmethod
    def get_student_count(lesson_group):
        try:
            student_count = lesson_group.lesson_group_plan.count()
            return student_count
        except AttributeError:
            return None

    class Meta:
        model = LessonGroup
        fields = (
            'pk',
            'teacher',
            'title',
            'student_limit',
            'send_message_on_no_payment',
            'schedules',
            'created_date',
            'student_plans',
            'student_count',
        )
        read_only_fields = ('pk', 'send_message_on_no_payment', 'schedules', 'created_date', 'student_plans',
                            'student_count')


class GroupReplacementSerializer(serializers.ModelSerializer):

    user_info = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_user_info(instance):
        try:
            return UserShortSerializer(instance.teacher.user).data
        except AttributeError:
            return None

    class Meta:
        model = GroupReplacement
        fields = (
            'pk',
            'lesson_group',
            'teacher',
            'date',
            'created_date',
            'user_info'
        )
        read_only_fields = ('pk', 'created_date',)

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        group_replacement = GroupReplacement(**validated_data)
        group_replacement.save(user_pk=user_pk)
        return group_replacement

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


class DayOffSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayOff
        fields = (
            'pk',
            'date',
            'comment',
            'created_date'
        )
        read_only_fields = ('pk', 'created_date')

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        day_off = DayOff(**validated_data)
        day_off.save(user_pk=user_pk)
        return day_off

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


class GroupTimeTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupTimeTransfer
        fields = (
            'pk',
            'lesson_group',
            'from_date',
            'to_date',
            'created_date',
        )
        read_only_fields = ('pk', 'created_date')

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        group_time_transfer = GroupTimeTransfer(**validated_data)
        group_time_transfer.save(user_pk=user_pk)
        return group_time_transfer

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
