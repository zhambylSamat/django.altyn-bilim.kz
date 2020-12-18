from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from ..models import (
    Subject,
    Topic,
    Video
)
from portal.api.constants import (
    FULL_STAFF_ROLES,
    TEACHER_ROLE,
)
from portal.api.utils import permission
from .serializers import SubjectSerializer, ChapterAndTopicSerializer, FullSubjectSerializer


class SubjectListView(APIView):

    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)

        subjects = Subject.objects.all().order_by('title')
        subject_serializer = SubjectSerializer(subjects, many=True)

        return Response(subject_serializer.data, status=200)


class ChaptersAndTopicsListView(APIView):
    permission_classes = (TokenHasReadWriteScope,)

    def get(self, request, subject_pk):
        roles = FULL_STAFF_ROLES
        permission(roles, request.user)
        chapters = Topic.objects.filter(subject__pk=subject_pk).order_by('order')
        chapter_serializer = ChapterAndTopicSerializer(chapters, many=True)
        return Response(chapter_serializer.data, status=200)


class FullSubjectListView(APIView):

    permission_classes = (TokenHasReadWriteScope, )

    def get(self, request):
        roles = (TEACHER_ROLE,)
        permission(roles, request.user)

        subjects = Subject.objects.all().order_by('title')
        subjects_serializers = FullSubjectSerializer(subjects, many=True)
        return Response(subjects_serializers.data, status=200)


# from portal.api.constants import DEVELOPER_ROLE
# from django.db.models import Q
# class SetUnreachedMidCotrolTopicsView(APIView):
#
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#
#         json = request.data.copy()
#
#         for subject_elem in json:
#             subject_title = subject_elem['subject']
#             topics = subject_elem['topics']
#             for topic_elem in topics:
#                 parent_topic_title = topic_elem['parent']
#                 sibling_topic_title = topic_elem['sibling']
#                 topic_title = topic_elem['topic']
#                 try:
#                     if parent_topic_title is not None:
#                         Topic.objects.get(Q(parent__title=parent_topic_title)
#                                           & Q(title=topic_title))
#                     else:
#                         Topic.objects.get(Q(subject__title=subject_title)
#                                           & Q(title=topic_title))
#                     pass
#                 except Topic.DoesNotExist:
#                     if sibling_topic_title is not None:
#                         if parent_topic_title is not None:
#                             sibling_topic_ent = Topic.objects.get(title=sibling_topic_title)
#                             parent_topic_ent = Topic.objects.get(title=parent_topic_title)
#                             self.reset_topic_order(None, parent_topic_ent, sibling_topic_ent.order, request.user.pk)
#                             topic_new_ent = Topic()
#                             topic_new_ent.subject = None
#                             topic_new_ent.parent = parent_topic_ent
#                             topic_new_ent.title = topic_title
#                             topic_new_ent.is_endpoint = True
#                             topic_new_ent.is_mid_control = True
#                             topic_new_ent.order = sibling_topic_ent.order + 1
#                             topic_new_ent.save(user_pk=request.user.pk)
#                         else:
#                             subject_ent = Subject.objects.get(title=subject_title)
#                             print(sibling_topic_title)
#                             sibling_topic_ent = Topic.objects.get(Q(parent__isnull=True)
#                                                                   & Q(title=sibling_topic_title))
#                             self.reset_topic_order(subject_ent, None, sibling_topic_ent.order, request.user.pk)
#                             topic_new_ent = Topic()
#                             topic_new_ent.subject = subject_ent
#                             topic_new_ent.parent = None
#                             topic_new_ent.title = topic_title
#                             topic_new_ent.is_endpoint = True
#                             topic_new_ent.is_mid_control = True
#                             topic_new_ent.order = sibling_topic_ent.order + 1
#                             topic_new_ent.save(user_pk=request.user.pk)
#                     if parent_topic_title is not None:
#                         print(parent_topic_title)
#                         parent_topic_ent = Topic.objects.get(Q(parent__isnull=True)
#                                                              & Q(title=parent_topic_title))
#                         topic_ent = Topic.objects.filter(parent=parent_topic_ent).order_by('order').last()
#                         topic_new_ent = Topic()
#                         topic_new_ent.subject = None
#                         topic_new_ent.parent = parent_topic_ent
#                         topic_new_ent.title = topic_title
#                         topic_new_ent.is_endpoint = True
#                         topic_new_ent.is_mid_control = True
#                         topic_new_ent.order = topic_ent.order + 1
#                         topic_new_ent.save(user_pk=request.user.pk)
#         return Response(status=201)
#
#     def reset_topic_order(self, subject, parent, order, user_pk):
#         if subject is not None:
#             topics = Topic.objects.filter(Q(subject=subject)
#                                           & Q(order__gt=order)).order_by('-order')
#             for topic in topics:
#                 topic.order += 1
#                 topic.save(user_pk=user_pk)
#         elif parent is not None:
#             topics = Topic.objects.filter(Q(parent=parent)
#                                           & Q(order__gt=order)).order_by('-order')
#             for topic in topics:
#                 topic.order += 1
#                 topic.save(user_pk=user_pk)





# from django.conf import settings
# import json
# class FetchExistingMaterials(APIView):
#     permission_classes = (TokenHasReadWriteScope,)
#
#     def post(self, request):
#         roles = (DEVELOPER_ROLE,)
#         permission(roles, request.user)
#         user_pk = request.user.pk
#         path = settings.BASE_DIR + '\material_json\\materials.txt'
#         f = open(path, 'r')
#         data_json = json.loads(f.read())
#         f.close()
#         subject_num = ''
#         subject = None
#         topic_num = ''
#         topic = None
#         subtopic_num = ''
#         subtopic = None
#
#         for item in data_json:
#             if subject_num != item['subject_num']:
#                 subject_num = item['subject_num']
#                 subject = Subject(title=item['subject_name']).save(user_pk=user_pk)
#             if topic_num != item['topic_num']:
#                 topic_num = item['topic_num']
#                 is_mid_control = True if item['quiz'] == 'y' else False
#                 is_endpoint = True if item['quiz'] == 'y' or int(item['subtopic_count']) <= 1 else False
#                 topic = Topic(subject=subject,
#                               parent=None,
#                               title=item['topic_name'],
#                               is_endpoint=is_endpoint,
#                               is_mid_control=is_mid_control,
#                               order=item['topic_order']).save(user_pk=user_pk)
#             if subtopic_num != item['subtopic_num'] and item['quiz'] == 'n' and int(item['subtopic_count']) > 1:
#                 subtopic_num = item['subtopic_num']
#                 subtopic = Topic(subject=None,
#                                  parent=topic,
#                                  title=item['subtopic_name'],
#                                  is_endpoint=True,
#                                  is_mid_control=False,
#                                  order=item['subtopic_order']).save(user_pk=user_pk)
#             if item['video_link']:
#                 timer_arr = item['timer'].split(':')
#                 duration = 0
#                 if len(timer_arr) == 3:
#                     duration = int(timer_arr[0]) * 3600 + int(timer_arr[1]) * 60 + int(timer_arr[2])
#                 if len(timer_arr) == 2:
#                     duration = int(timer_arr[0]) * 60 + int(timer_arr[1])
#                 if len(timer_arr) == 1:
#                     duration = int(timer_arr[0])
#                 video = Video(topic=subtopic,
#                               title=None,
#                               duration=duration,
#                               link=item['video_link']).save(user_pk=user_pk)
#         return Response(status=201)
