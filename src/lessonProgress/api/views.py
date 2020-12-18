from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from portal.api.utils import permission, monthdelta
import datetime
from django.db.models import Q

from django.contrib.auth.models import User
from portal.api.constants import TEACHER_ROLE, STUDENT_ROLE, DEVELOPER_ROLE, FULL_STAFF_ROLES
from ..models import GroupStudentVisit, StudentVisit, TopicQuizMark, TrialTest, TrialTestMark, LessonVideoAction
from groupsAndLessons.models import (
    LessonGroup,
    LessonGroupStudent,
    LessonGroupSchedule,
    TopicPlan,
    GroupReplacement,
    SubjectPlan,
    StudentPlan,
    DayOff,
    GroupTimeTransfer,
)
from materials.models import Subject, Topic
from configuration.models import SubjectQuizConfiguration
from configuration.api.serializers import SubjectQuizConfigurationSerializer
from .serializers import (
    LessonGroupStudentsABSSerializer,
    LessonGroupStudentsABSEditSerializer,
    GroupStudentVisitSerializer,
    StudentVisitSerializer,
    GroupWithStudentVisitSerializer,
    TopicQuizByTopicPlanListSerializer,
    TopicQuizMarkSerializer,
    TrialTestSerializer,
    TrialTestMarkSerializer,
    LessonVideoActionSerializer
)
from materials.api.serializers import VideoSerializer, TopicSerializer, SubjectSerializer
from portal.api.constants import WEEK_DAY_CHOICES
from portal.api.serializer import UserShortSerializer
from groupsAndLessons.api.utils import recalculate_student_plan_progress_by_student_plan
from .utils import get_day_sign_by_num, has_access_to_video, set_ip, check_ip, remove_all_student_video_access
from portal.api.utils import get_day_id_from_date, increase_one_day_in_date


class StudentsABSView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, group_id):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        group_student_visit_count = GroupStudentVisit.objects.filter(lesson_group__pk=group_id).count()

        result = {
            'date': None,
            'group_student_visit': None,
            'day_name': None,
            'students': []
        }

        lesson_group_schedule_day_ids = [ent.schedule.week_num
                                         for ent
                                         in LessonGroupSchedule.objects.filter(group_schedule__lesson_group__pk=group_id)]
        lesson_group = LessonGroup.objects.get(pk=group_id)
        if group_student_visit_count:
            group_student_visit = GroupStudentVisit.objects.filter(lesson_group__pk=group_id).order_by('-abs_date').first()
            last_abs_date = group_student_visit.abs_date
            last_abs_date = increase_one_day_in_date(last_abs_date)
            while get_day_id_from_date(last_abs_date) not in lesson_group_schedule_day_ids \
                    or GroupReplacement.objects.filter(lesson_group=lesson_group, date=last_abs_date, teacher__isnull=True).exists() \
                    or DayOff.objects.filter(date=last_abs_date).exists():
                last_abs_date = increase_one_day_in_date(last_abs_date)
            else:
                if last_abs_date <= datetime.date.today():
                    transfer_date = None
                    try:
                        group_time_transfer = GroupTimeTransfer.objects.get(
                            Q(lesson_group=group_student_visit.lesson_group)
                            & Q(from_date=last_abs_date))
                        transfer_date = group_time_transfer.to_date
                    except GroupTimeTransfer.DoesNotExist:
                        pass
                    day_sign = get_day_sign_by_num(get_day_id_from_date(last_abs_date))
                    lesson_group_students = LessonGroupStudent.objects.filter(Q(lesson_group__pk=group_id)
                                                                              & Q(started_date__lte=last_abs_date)
                                                                              & Q(short_schedule__week_day_sign=day_sign))
                    total_abs_date = transfer_date if transfer_date else last_abs_date
                    lesson_group_students_serializers = LessonGroupStudentsABSSerializer(lesson_group_students,
                                                                                         many=True, context={
                                                                                            'abs_date': total_abs_date})
                    result['date'] = total_abs_date
                    result['day_name'] = dict(WEEK_DAY_CHOICES)[get_day_id_from_date(total_abs_date)]
                    result['students'] = lesson_group_students_serializers.data
                    return Response(result, status=200)
                else:
                    return Response(result, status=200)
        else:
            lesson_group_students = LessonGroupStudent.objects.filter(lesson_group__pk=group_id).order_by('started_date')
            if lesson_group_students.count():
                abs_date = lesson_group_students.first().started_date
                while get_day_id_from_date(abs_date) not in lesson_group_schedule_day_ids \
                        or GroupReplacement.objects.filter(lesson_group=lesson_group, date=abs_date, teacher__isnull=True).exists() \
                        or DayOff.objects.filter(date=abs_date).exists():
                    abs_date = increase_one_day_in_date(abs_date)
                else:
                    if abs_date <= datetime.date.today():
                        transfer_date = None
                        try:
                            group_time_transfer = GroupTimeTransfer.objects.get(
                                Q(lesson_group=lesson_group_students.first().lesson_group)
                                & Q(from_date=abs_date))
                            transfer_date = group_time_transfer.to_date
                        except GroupTimeTransfer.DoesNotExist:
                            pass
                        day_sign = get_day_sign_by_num(get_day_id_from_date(abs_date))
                        lesson_group_students = lesson_group_students.filter(Q(started_date__lte=abs_date)
                                                                             & Q(short_schedule__week_day_sign=day_sign))
                        total_abs_date = transfer_date if transfer_date else abs_date
                        lesson_group_students_serializers = LessonGroupStudentsABSSerializer(lesson_group_students,
                                                                                             many=True, context={
                                                                                            'abs_date': total_abs_date})
                        result['date'] = total_abs_date
                        result['day_name'] = dict(WEEK_DAY_CHOICES)[get_day_id_from_date(total_abs_date)]
                        result['students'] = lesson_group_students_serializers.data
                        return Response(result, status=200)
                    else:
                        return Response(result, status=200)

    def post(self, request):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        group_student_visit_serializer = GroupStudentVisitSerializer(data=request.data['group_student_visit'].copy())
        student_visit_serializer = StudentVisitSerializer(data=request.data['student_visit'].copy(), many=True)

        errors = {'error': []}
        if not group_student_visit_serializer.is_valid():
            errors['error'].append(group_student_visit_serializer.errors)
        elif not student_visit_serializer.is_valid():
            errors['error'].append(student_visit_serializer.errors)
        else:
            group_student_visit = group_student_visit_serializer.save(user_pk=request.user.pk)
            student_visit_serializer.save(user_pk=request.user.pk, group_student_visit=group_student_visit)
            message = {'message': ['Орындалды']}
            return Response(message, status=201)
        return Response(errors, status=400)

    def put(self, request):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)
        errors = {'error': []}

        try:
            group_student_visit = GroupStudentVisit.objects.get(pk=request.data['group_student_visit']['pk'])
            for sv_json in request.data['student_visit'].copy():
                if sv_json['pk']:
                    try:
                        student_visit = StudentVisit.objects.get(pk=sv_json['pk'])
                        student_visit_serializer = StudentVisitSerializer(student_visit,
                                                                          data=sv_json.copy(),
                                                                          many=False,
                                                                          partial=True)
                        if not student_visit_serializer.is_valid():
                            errors['error'].append(student_visit_serializer.errors)
                        else:
                            student_visit_serializer.save(user_pk=request.user.pk)
                    except StudentVisit.DoesNotExist:
                        return Response(status=404)
                else:
                    student_visit_serializer = StudentVisitSerializer(data=sv_json.copy(), many=False)
                    if not student_visit_serializer.is_valid():
                        errors['error'].append(student_visit_serializer.errors)
                    else:
                        student_visit_serializer.save(user_pk=request.user.pk, group_student_visit=group_student_visit)
            if errors['error']:
                return Response(errors, status=400)
            else:
                message = {'message': ['Орындалды']}
                return Response(message, status=201)

        except GroupStudentVisit.DoesNotExist:
            return Response(status=404)


class StudentABSEditView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, group_student_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)
        result = {
            'date': None,
            'group_student_visit': None,
            'day_name': None,
            'students': []
        }
        try:
            access_to_edit_time = datetime.date.today()
            group_student_visit = GroupStudentVisit.objects.get(Q(pk=group_student_pk))
            if group_student_visit.created_date.date() == access_to_edit_time:
                day_sign = get_day_sign_by_num(get_day_id_from_date(group_student_visit.abs_date))
                lesson_group_students = LessonGroupStudent.objects.filter(Q(lesson_group=group_student_visit.lesson_group)
                                                                          & Q(started_date__lte=group_student_visit.abs_date)
                                                                          & Q(short_schedule__week_day_sign=day_sign))

                lesson_group_students_serializers = LessonGroupStudentsABSEditSerializer(lesson_group_students, many=True, context={'abs_date': group_student_visit.abs_date})
                result['date'] = group_student_visit.abs_date
                result['group_student_visit'] = group_student_pk
                result['day_name'] = dict(WEEK_DAY_CHOICES)[self.get_day_id_in_date(group_student_visit.abs_date)]
                result['students'] = lesson_group_students_serializers.data
                return Response(result, status=200)
            else:
                error = {'error': "Өзгертуге болатын уақыт аяқталды!"}
                return Response(error, status=400)
        except GroupStudentVisit.DoesNotExist:
            return Response(status=404)

    @staticmethod
    def get_day_id_in_date(date):
        day_id = date.strftime('%w')
        day_id = 7 if day_id == 0 else day_id
        return int(day_id)


class StudentABSMonthListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, lesson_group_pk):
        roles = (TEACHER_ROLE,)
        roles += FULL_STAFF_ROLES
        permission(roles, request.user)
        current = datetime.date.today().replace(day=1)
        end = monthdelta(current, 1)
        start = monthdelta(end, -12)
        group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group__pk=lesson_group_pk)
                                                               & Q(abs_date__lt=end)
                                                               & Q(abs_date__gte=start)).order_by('-abs_date')
        year_month = []
        for item in group_student_visit:
            tmp = item.abs_date.strftime('%Y-%m')
            if tmp not in year_month:
                year_month.append(tmp)
        return Response(year_month, status=200)


class StudentABSListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, lesson_group_pk, date):
        roles = (TEACHER_ROLE,)
        roles += FULL_STAFF_ROLES
        permission(roles, request.user)
        result = {'dates': None, 'students': None}
        if date == 'current':
            current_date = datetime.date.today().replace(day=1)
            group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group__pk=lesson_group_pk)).order_by('-abs_date')
            if group_student_visit.count() != 0:
                while group_student_visit.filter(Q(abs_date__gte=current_date)).count() == 0:
                    current_date = monthdelta(current_date, -1)
                group_student_visit = group_student_visit.filter(Q(abs_date__month=current_date.month)
                                                                 & Q(abs_date__year=current_date.year))
        else:
            current_date = datetime.datetime.strptime(date+'-01', '%Y-%m-%d')
            group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group__pk=lesson_group_pk)
                                                                   & Q(abs_date__month=current_date.month)
                                                                   & Q(abs_date__year=current_date.year)).order_by('-abs_date')

        group_student_visit_serializer = GroupWithStudentVisitSerializer(group_student_visit, many=True)
        students = []
        for gsv in group_student_visit:
            for sv in gsv.group_student_visit.all():
                student = sv.lesson_group_student.student_plan.student
                if student not in students:
                    students.append(student)
        students = sorted(students, key=lambda elem: elem.pk)
        students_serializer = UserShortSerializer(students, many=True)
        result = {'dates': group_student_visit_serializer.data, 'students': students_serializer.data}
        return Response(result, status=200)


class SetStudentPlanDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def put(self, request, topic_plan, action, mark):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)
        try:
            topic_plan = TopicPlan.objects.get(pk=topic_plan)
            if action == 'tutorial':
                topic_plan.tutorial = mark
            elif action == 'class_work':
                topic_plan.class_work = mark
            elif action == 'home_work':
                topic_plan.home_work = mark
            else:
                return Response(status=404)
            topic_plan.save(user_pk=request.user.pk)
            recalculate_student_plan_progress_by_student_plan(topic_plan.subject_plan.student_plan, request.user.pk)
            return Response(status=201)
        except TopicPlan.DoesNotExist:
            return Response(status=404)


class TopicQuizPlanDetailView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, subject_plan_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        try:
            subject_plan = SubjectPlan.objects.get(pk=subject_plan_pk)
            subject_quiz_configuration = SubjectQuizConfiguration.objects.get(subject=subject_plan.subject)
            subject_quiz_configuration_serializer = SubjectQuizConfigurationSerializer(subject_quiz_configuration,
                                                                                       many=False)
            topic_plan = subject_plan.topic_plan.filter(topic__is_mid_control=True)
            topic_plan_tmp = {}
            for ent in topic_plan:
                topic = ent.topic
                if topic.parent is not None:
                    topic_plan_tmp[topic.parent.order] = ent
                else:
                    topic_plan_tmp[topic.order] = ent
            topic_plan = [topic_plan_tmp[key] for key in sorted(topic_plan_tmp.keys())]

            topic_quiz_mark_by_topic_plan_serializer = TopicQuizByTopicPlanListSerializer(topic_plan, many=True)
            result = {
                'config': subject_quiz_configuration_serializer.data,
                'quiz': topic_quiz_mark_by_topic_plan_serializer.data
            }
            return Response(result, status=200)
        except SubjectQuizConfiguration.DoesNotExist:
            return Response(status=403)
        except SubjectPlan.DoesNotExist:
            return Response(status=401)

    def post(self, request):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        topic_quiz_mark_serializer = TopicQuizMarkSerializer(data=request.data.copy(), many=False)
        if topic_quiz_mark_serializer.is_valid():
            topic_quiz_mark_serializer.save(user_pk=request.user.pk)
            result = {
                'topic_quiz_mark': topic_quiz_mark_serializer.data,
                'message': 'Аралық бақылау бағасы енгізілді'
            }
            return Response(result, status=201)

        return Response(topic_quiz_mark_serializer.error, status=400)

    def put(self, request, topic_quiz_mark_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        try:
            topic_quiz_mark = TopicQuizMark.objects.get(pk=topic_quiz_mark_pk)
            topic_quiz_mark_serializer = TopicQuizMarkSerializer(topic_quiz_mark, data=request.data.copy(), partial=True, many=False)
            topic_plan_pk = request.data['topic_plan']
            subject_plan = TopicPlan.objects.get(pk=topic_plan_pk).subject_plan
            student_plan = subject_plan.student_plan
            lesson_group_student = LessonGroupStudent.objects.filter(student_plan=student_plan)
            no_abs = True
            for ent in lesson_group_student:
                lesson_group = ent.lesson_group
                group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group=lesson_group)
                                                                       & Q(abs_date__gt=datetime.date.today())
                                                                       & Q(group_student_visit__attendance=True))
                if len(group_student_visit) != 0:
                    no_abs = False
                    break
            if no_abs:
                if topic_quiz_mark_serializer.is_valid():
                    topic_quiz_mark_serializer.save(user_pk=request.user.pk)
                    result = {
                        'topic_quiz_mark': topic_quiz_mark_serializer.data,
                        'message': 'Аралық бақылаудың бағасы өзгертілді'
                    }
                    return Response(result, status=201)
                return Response(topic_quiz_mark_serializer.errors, status=400)
            else:
                result = 'Аралық бақылаудың бағасын өзгерту мүмкін емес'
                return Response(result, status=400)

        except TopicQuizMark.DoesNotExist:
            return Response(status=404)

    def delete(self, request, topic_quiz_mark_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        try:
            topic_quiz_mark = TopicQuizMark.objects.get(pk=topic_quiz_mark_pk)
            subject_plan = topic_quiz_mark.topic_plan.subject_plan
            student_plan = subject_plan.student_plan
            lesson_group_student = LessonGroupStudent.objects.filter(student_plan=student_plan)
            no_abs = True
            for ent in lesson_group_student:
                lesson_group = ent.lesson_group
                group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group=lesson_group)
                                                                       & Q(abs_date__gt=datetime.date.today())
                                                                       & Q(group_student_visit__attendance=True))
                if len(group_student_visit) != 0:
                    no_abs = False
                    break
            if no_abs:
                topic_quiz_mark.delete(user_pk=request.user.pk)
                topic_quiz_mark_serializer = TopicQuizMarkSerializer(None)
                result = {
                    'topic_quiz_mark': topic_quiz_mark_serializer.data,
                    'message': 'Аралық бақылаудың бағасы өшірілді'
                }
                return Response(result, status=201)
            else:
                result = 'Аралық бақылаудың бағасын өшіру мүмкін емес'
                return Response(result, status=400)
        except TopicQuizMark.DoesNotExist:
            return Response(status=404)


class TrialTestByStudentAndSubjectListView(APIView):

    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, student_pk, subject_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        try:
            trial_test = TrialTest.objects.get(Q(student__pk=student_pk)
                                               & Q(subject__pk=subject_pk))
        except TrialTest.DoesNotExist:
            try:
                student_user = User.objects.get(pk=student_pk)
                subject = Subject.objects.get(pk=subject_pk)
            except User.DoesNotExist:
                return Response(status=404)
            except Subject.DoesNotExist:
                return Response(status=404)
            trial_test = TrialTest(student=student_user, subject=subject)
            trial_test.save(user_pk=request.user.pk)

        trial_test_serializer = TrialTestSerializer(trial_test)
        return Response(trial_test_serializer.data, status=200)

    def post(self, request):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        trial_test_mark_serializer = TrialTestMarkSerializer(data=request.data.copy())
        if trial_test_mark_serializer.is_valid():
            trial_test_mark_serializer.save(user_pk=request.user.pk)
            result = {
                'trial_test_mark': trial_test_mark_serializer.data,
                'message': 'Пробный тесттің бағасы енгізілді'
            }
            return Response(result, status=201)
        return Response(trial_test_mark_serializer.errors, status=400)

    def put(self, request, trial_test_mark_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        try:
            trial_test_mark = TrialTestMark.objects.get(pk=trial_test_mark_pk)
            trial_test_mark_serializer = TrialTestMarkSerializer(trial_test_mark, data=request.data.copy(), partial=True)

            student_plan = StudentPlan.objects.get(Q(student=trial_test_mark.trial_test.student)
                                                   & Q(subject=trial_test_mark.trial_test.subject))
            lesson_group_student = LessonGroupStudent.objects.filter(student_plan=student_plan)
            no_abs = True
            for ent in lesson_group_student:
                lesson_group = ent.lesson_group
                group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group=lesson_group)
                                                                       & Q(abs_date__gt=datetime.date.today())
                                                                       & Q(group_student_visit__attendance=True))
                if len(group_student_visit) != 0:
                    no_abs = False
                    break
            if no_abs:
                if trial_test_mark_serializer.is_valid():
                    trial_test_mark_serializer.save(user_pk=request.user.pk)
                    result = {
                        'trial_test_mark': trial_test_mark_serializer.data,
                        'message': 'Пробный тест бағасы өзгертілді'
                    }
                    return Response(result, status=201)
                return Response(trial_test_mark_serializer.error, status=400)
            else:
                result = 'Пробный тесттің бағасын өзгерту мүмкін емес'
                return Response(result, status=400)
        except TrialTestMark.DoesNotExist:
            return Response(status=404)

    def delete(self, request, trial_test_mark_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        try:
            trial_test_mark = TrialTestMark.objects.get(pk=trial_test_mark_pk)
            student_plan = StudentPlan.objects.get(Q(student=trial_test_mark.trial_test.student)
                                                   & Q(subject=trial_test_mark.trial_test.subject))
            lesson_group_student = LessonGroupStudent.objects.filter(student_plan=student_plan)
            no_abs = True
            for ent in lesson_group_student:
                lesson_group = ent.lesson_group
                group_student_visit = GroupStudentVisit.objects.filter(Q(lesson_group=lesson_group)
                                                                       & Q(abs_date__gt=datetime.date.today())
                                                                       & Q(group_student_visit__attendance=True))
                if len(group_student_visit) != 0:
                    no_abs = False
                    break
            if no_abs:
                trial_test_mark.delete(user_pk=request.user.pk)
                trial_test_mark_serializer = TrialTestMarkSerializer(None)
                result = {
                    'trial_test_mark': trial_test_mark_serializer.data,
                    'message': 'Пробный тесттің бағасы өшірілді'
                }
                return Response(result, status=200)
            else:
                result = "Пробный тесттің бағасын өшіру мүмкін емес"
                return Response(result, status=400)

        except TrialTestMark.DoesNotExist:
            return Response(status=404)


class StudentVideoActionListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, student_user_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        video_actions = LessonVideoAction.objects.filter(lesson_group_student__student_plan__student=student_user_pk)

        video_actions_serializer = LessonVideoActionSerializer(video_actions, many=True)
        return Response(video_actions_serializer.data, status=200)


class StudentVideoActionDetailView(APIView):

    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request, lesson_group_student_pk, topic_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        try:
            lesson_video_action = LessonVideoAction.objects.get(Q(lesson_group_student__pk=lesson_group_student_pk)
                                                                & Q(topic__pk=topic_pk))
            lesson_video_action.delete(user_pk=request.user.pk)
        except LessonVideoAction.DoesNotExist:
            pass

        try:
            lesson_group_student = LessonGroupStudent.objects.get(pk=lesson_group_student_pk)
            topic = Topic.objects.get(Q(pk=topic_pk) & Q(is_endpoint=True))
            lesson_group = lesson_group_student.lesson_group
            set_ip(lesson_group, request.META, request.user.pk)
            if has_access_to_video(lesson_group):
                if topic.t_video.all().count() != 0:
                    lesson_video_action = LessonVideoAction(lesson_group_student=lesson_group_student,
                                                            topic=topic)
                    lesson_video_action.save(user_pk=request.user.pk)
                    user = lesson_group_student.student_plan.student
                    video_action_serializer = LessonVideoActionSerializer(lesson_video_action, many=False)
                    result = {
                        'message': 'Оқушыға ({} {}) "{}" тақырыбына қатысты видео сабақ жіберілді'.format(
                            user.last_name,
                            user.first_name,
                            topic.title),
                        'video_action': video_action_serializer.data
                    }
                    return Response(result, status=201)
                result = 'Видео енгізілмеген'
                return Response(result, status=400)
            else:
                result = 'Доступ ашуға болатын уақыт бітті'
                return Response(result, status=400)
        except LessonGroupStudent.DoesNotExist:
            return Response(status=404)
        except Topic.DoesNotExist:
            return Response(status=404)

    def delete(self, request, lesson_video_action_pk):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        try:
            lesson_video_action = LessonVideoAction.objects.get(pk=lesson_video_action_pk)
            user = lesson_video_action.lesson_group_student.student_plan.student
            topic = lesson_video_action.topic
            lesson_video_action.delete(user_pk=request.user.pk)
            result = {
                'message': 'Оқушыдан ({} {}) "{}" тақырыбына қатысты видео сабақ өшірілді'.format(user.last_name,
                                                                                                  user.first_name,
                                                                                                  topic.title)
            }
            return Response(result, status=201)
        except LessonVideoAction.DoesNotExist:
            return Response(status=404)


class StudentVideoListView(APIView):

    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = (STUDENT_ROLE,)
        permission(roles, request.user)

        lesson_video_actions = LessonVideoAction.objects.filter(
            lesson_group_student__student_plan__student=request.user).order_by('topic__order')

        result = {}

        for ent in lesson_video_actions:
            lesson_group = ent.lesson_group_student.lesson_group
            if has_access_to_video(lesson_group):
                topic = ent.topic
                if ent.topic.parent is not None:
                    topic = ent.topic.parent
                if topic.subject.pk not in result:
                    result[topic.subject.pk] = {
                        'subject': SubjectSerializer(topic.subject, many=False).data,
                        'topics': {}
                    }
                if topic.order not in result[topic.subject.pk]['topics']:
                    result[topic.subject.pk]['topics'][topic.order] = []
                ip_success = check_ip(lesson_group, request.META)
                result[topic.subject.pk]['topics'][topic.order].append({
                    'topic': TopicSerializer(ent.topic, many=False).data,
                    'video': VideoSerializer(ent.topic.t_video.all(), many=True).data if ip_success else None,
                    'has_video': True,
                    'ip_success': ip_success,
                    'message': 'IP адресс мұғалімдікімен сәйкес келмейді. Мұғалімге айт' if not ip_success else ''
                })

        result = dict(sorted(result.items(), key=lambda subject: subject[1]['subject']['title']))
        for subject_key, subject_val in result.items():
            result[subject_key]['topics'] = dict(sorted(subject_val['topics'].items(), key=lambda elem: elem[0]))
            last_order = list(result[subject_key]['topics'])[-1]
            last_topic = result[subject_key]['topics'][last_order][-1]['topic']
            result[subject_key]['topics'] = list(result[subject_key]['topics'].values())
            tmp = []
            for i in range(len(result[subject_key]['topics'])):
                for item in result[subject_key]['topics'][i]:
                    if item not in tmp:
                        tmp.append(item)
            result[subject_key]['topics'] = tmp

            if last_topic['parent'] is not None:
                try:
                    tmp_topic = Topic.objects.get(Q(parent__pk=last_topic['parent']) & Q(order=last_topic['order'] + 1))
                    video_count = tmp_topic.t_video.all().count()
                    result[subject_key]['topics'].append({
                        'topic': TopicSerializer(tmp_topic, many=False).data,
                        'video': None,
                        'has_video': False if video_count == 0 else True
                    })
                except Topic.DoesNotExist:
                    pass
            else:
                try:
                    tmp_topic = Topic.objects.get(Q(subject__pk=last_topic['subject']) & Q(order=last_topic['order'] + 1))
                    video_count = tmp_topic.t_video.all().count()
                    result[subject_key]['topics'].append({
                        'topic': TopicSerializer(tmp_topic, many=False).data,
                        'video': None,
                        'has_video': False if video_count == 0 else True
                    })
                except Topic.DoesNotExist:
                    pass
        result = list(result.values())
        return Response(result, status=200)


class RemoveAllStudentVideoActionsView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def post(self, request):
        roles = (DEVELOPER_ROLE,)
        permission(roles, request.user)
        remove_all_student_video_access()
        return Response(status=201)


# 0005_auto_20191113_1729

#
# from rest_framework.permissions import AllowAny
# import requests
# class InsertTrialTests(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         url = "https://old.altyn-bilim.kz/test2/getTrialTestNotifications.php"
#         responses = requests.get(url).json()
#
#         for response in responses:
#             last_name = response['surname']
#             first_name = response['name']
#             title = response['subject_name']
#             mark = response['mark']
#             created_date = response['date_of_test']
#             try:
#                 student_user = User.objects.get(Q(last_name=last_name) & Q(first_name=first_name))
#                 subject = Subject.objects.get(title=title)
#                 try:
#                     trial_test = TrialTest.objects.get(Q(subject=subject) & Q(student=student_user))
#                 except TrialTest.DoesNotExist:
#                     trial_test = TrialTest(subject=subject,
#                                            student=student_user)
#                     trial_test.save()
#                 trial_test_mark = TrialTestMark(trial_test=trial_test,
#                                                 mark=mark,
#                                                 date=created_date,
#                                                 created_date=created_date)
#                 trial_test_mark.save()
#             except User.DoesNotExist:
#                 pass
#             except Subject.DoesNotExist:
#                 return Response(status=400)
#
#         return Response(responses, status=200)
#
#
# class FetchTopicQuiz(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         url = "https://old.altyn-bilim.kz/test2/getSubjectQuiz.php"
#         responses = requests.get(url).json()
#
#         for response in responses:
#             last_name = response['surname']
#             first_name = response['name']
#             topic_title = response['topic_name'].strip()
#             subject_title = response['subject_name']
#             theory = response['mark_theory']
#             practice = response['mark_practice']
#             created_date = response['created_date']
#             # print(title)
#             # title = ' '.join(title.split(' ')[1:])
#             if topic_title == 'Өрнекті ықшамдау, рационал бөлшек теңдеулер, теңсіздіктер, теңсіздіктер жүйесі':
#                 topic_title = 'Өрнекті ықшамдау, теңдеулер, теңсіздіктер, теңсіздіктер жүйесі'
#             elif topic_title == 'Интеграл':
#                 topic_title = 'Аралық бақылау. Интеграл. Функция'
#             elif topic_title == '№1':
#                 topic_title = 'Аралық бақылау 1'
#             elif topic_title == '№2':
#                 topic_title = 'Аралық бақылау 2'
#             elif topic_title == '№3':
#                 topic_title = 'Аралық бақылау 3'
#             elif topic_title == 'Оптика. Фотоэффект':
#                 topic_title = 'Аралық бақылау. Опитка. Фотоэффект.'
#             try:
#                 student_user = User.objects.get(Q(last_name=last_name)
#                                                 & Q(first_name=first_name))
#                 try:
#                     subject_plan = SubjectPlan.objects.get(Q(student_plan__student=student_user)
#                                                            & Q(subject__title=subject_title))
#                     topic_plan = TopicPlan.objects.get(Q(subject_plan=subject_plan)
#                                                        & Q(topic__title__endswith=topic_title)
#                                                        & Q(topic__is_mid_control=True))
#                     print('asdfasdfasdfasdf', topic_plan.topic.title)
#                     try:
#                         TopicQuizMark.objects.get(topic_plan=topic_plan,
#                                                   practice=practice,
#                                                   theory=theory,
#                                                   created_date=created_date)
#                     except TopicQuizMark.DoesNotExist:
#                         topic_quiz_mark = TopicQuizMark(topic_plan=topic_plan,
#                                                         practice=practice,
#                                                         theory=theory,
#                                                         created_date=created_date)
#                         topic_quiz_mark.save()
#                 except SubjectPlan.DoesNotExist:
#                     pass
#                 except SubjectPlan.MultipleObjectsReturned:
#                     subject_plan = SubjectPlan.objects.filter(Q(student_plan__student=student_user)
#                                                            & Q(subject__title=subject_title))
#                     print(student_user, subject_title)
#                     print(subject_plan)
#                     return Response(['SubjectPlan.MultipleObjectsReturned', student_user], status=400)
#                 except TopicPlan.DoesNotExist:
#                     print(last_name, first_name, topic_title, ':', response['topic_name'], theory, practice,
#                           created_date)
#                     print(student_user)
#                     print(subject_plan)
#                     topic = Topic.objects.filter(Q(title__endswith=topic_title) & Q(is_mid_control=True))
#                     print(topic)
#                     return Response(['TopicPlan.DoesNotExist'], status=400)
#                 except TopicPlan.MultipleObjectsReturned:
#                     topic_plan = TopicPlan.objects.filter(Q(subject_plan__student_plan__student=student_user)
#                                                           & Q(topic__title__endswith=topic_title)
#                                                           & Q(topic__is_mid_control=True))
#                     for ent in topic_plan:
#                         print(ent.topic.title)
#                     return Response(['TopicPlan.MultipleObjectsReturned'], status=400)
#             except User.DoesNotExist:
#                 pass
#
#         return Response(responses, status=200)


# from portal.api.constants import DEVELOPER_ROLE
# from ..models import StudentVisitHistory
# from groupsAndLessons.models import LessonGroupStudentHistory, LessonGroupStudentShortScheduleHistory, StudentPlanHistory
# from django.contrib.auth.models import User
# class RemoveUnnecessaryStudentVisitView(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#     def get(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#         student_visit_histories = StudentVisitHistory.objects.all()
#         count = 0
#         import json
#         import io
#         total_result = ''
#         for student_visit_history in student_visit_histories:
#             group_visit = GroupStudentVisit.objects.get(pk=student_visit_history.group_student_visit_id)
#             week_sign = None
#             lesson_group_student_pk = None
#             lesson_group_student_origin_id = None
#             full_name = None
#             try:
#                 lesson_group_student = LessonGroupStudent.objects.get(pk=student_visit_history.lesson_group_student_id)
#                 week_sign = [item.week_day_sign for item in lesson_group_student.short_schedule.all()]
#                 lesson_group_student_pk = lesson_group_student.pk
#                 full_name = lesson_group_student.student_plan.student.last_name + ' ' + lesson_group_student.student_plan.student.first_name,
#             except LessonGroupStudent.DoesNotExist:
#                 lesson_group_student_history = LessonGroupStudentHistory.objects.filter(origin_id=student_visit_history.lesson_group_student_id).order_by('updated_date').last()
#                 week_sign = [item.week_day_sign for item in LessonGroupStudentShortScheduleHistory.objects.filter(lesson_group_student_id=lesson_group_student_history.origin_id)]
#                 student_plan_history = StudentPlanHistory.objects.filter(origin_id=lesson_group_student_history.student_plan_id).order_by('updated_date').last()
#                 student_user = User.objects.get(pk=student_plan_history.student_id)
#                 full_name = student_user.last_name + ' ' + student_user.first_name
#                 lesson_group_student_origin_id = lesson_group_student_history.origin_id
#
#             count += 1
#             abs_week_num = get_day_sign_by_num(self.get_day_id_from_date(group_visit.abs_date))
#             abs_week_num = 3 if abs_week_num is None else abs_week_num
#             if abs_week_num not in week_sign:
#                 if lesson_group_student_pk:
#                     lesson_group_student.delete(user_pk=request.user.pk)
#                 student_visit_history_del = StudentVisitHistory.objects.filter(origin_id=student_visit_history.origin_id)
#                 history_id = [item.pk for item in student_visit_history_del]
#                 student_visit_history_del.delete()
#                 result = {
#                     'count': count,
#                     'type': 'delete',
#                     'abs_date': str(group_visit.abs_date),
#                     'group_title': group_visit.lesson_group.title,
#                     'abs_week_num': self.get_day_id_from_date(group_visit.abs_date),
#                     'abs_week_num_sign': abs_week_num,
#                     'week_sign': week_sign,
#                     'full_name': full_name,
#                     'lesson_group_student': lesson_group_student_pk,
#                     'lesson_group_student_origin_id': lesson_group_student_origin_id,
#                     'history_ids': history_id,
#                     'split': '--------------------------------------------------------'
#                 }
#                 result = json.dumps(result, ensure_ascii=False, indent=4)
#                 total_result += result
#         f = io.open('results.txt', 'w', encoding='utf8')
#         f.write(total_result)
#         f.close()
#
#         return Response(status=200)
#     @staticmethod
#     def get_day_id_from_date(date):
#         day_id = int(date.strftime('%w'))
#         day_id = 7 if day_id == 0 else day_id
#         return int(day_id)
