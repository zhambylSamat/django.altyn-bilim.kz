from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .utils import student_attendance_notification, topic_quiz_notification, trial_test_notification
from rest_framework.response import Response


# class CheckStudentAttendanceNotification(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#         for day in days:
#             student_attendance_notification('2020-03-'+day)
#         return Response(status=201)
#
#
# class CheckTopicQuizNotification(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#         for day in days:
#             topic_quiz_notification('2020-03-'+day)
#         return Response(status=201)
#
#
# class CheckTrialTestNotification(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#         for day in days:
#             trial_test_notification('2020-03-'+day)
#         return Response(status=201)
