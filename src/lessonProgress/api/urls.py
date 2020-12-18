from django.urls import path
from .views import (
    StudentsABSView,
    StudentABSListView,
    StudentABSMonthListView,
    StudentABSEditView,
    SetStudentPlanDetailView,
    TopicQuizPlanDetailView,
    TrialTestByStudentAndSubjectListView,
    StudentVideoActionListView,
    StudentVideoActionDetailView,
    StudentVideoListView,
    RemoveAllStudentVideoActionsView,

    # InsertTrialTests,
    # FetchTopicQuiz
    # RemoveUnnecessaryStudentVisitView
)

urlpatterns = [
    path('students/abs/<group_id>/', StudentsABSView.as_view()),
    path('students/edit/abs/<group_student_pk>/', StudentABSEditView.as_view()),
    path('students/abs/', StudentsABSView.as_view()),
    path('students/abs/update/', StudentsABSView.as_view()),
    path('students/abs/list/<lesson_group_pk>/<date>/', StudentABSListView.as_view()),
    path('students/abs/month/list/<lesson_group_pk>/', StudentABSMonthListView.as_view()),
    path('student/set/plan/<topic_plan>/<action>/<mark>/', SetStudentPlanDetailView.as_view()),
    path('student/plan/quiz/list/<subject_plan_pk>/', TopicQuizPlanDetailView.as_view()),
    path('student/plan/quiz/create/', TopicQuizPlanDetailView.as_view()),
    path('student/plan/quiz/edit/<topic_quiz_mark_pk>/', TopicQuizPlanDetailView.as_view()),
    path('student/plan/quiz/delete/<topic_quiz_mark_pk>/', TopicQuizPlanDetailView.as_view()),
    path('student/trial/test/list/<student_pk>/<subject_pk>/', TrialTestByStudentAndSubjectListView.as_view()),
    path('student/trial/test/create/', TrialTestByStudentAndSubjectListView.as_view()),
    path('student/trial/test/edit/<trial_test_mark_pk>/', TrialTestByStudentAndSubjectListView.as_view()),
    path('student/trial/test/delete/<trial_test_mark_pk>/', TrialTestByStudentAndSubjectListView.as_view()),
    path('student/video/action/list/<student_user_pk>/', StudentVideoActionListView.as_view()),
    path('student/video/action/set/<lesson_group_student_pk>/<topic_pk>/', StudentVideoActionDetailView.as_view()),
    path('student/video/action/delete/<lesson_video_action_pk>/', StudentVideoActionDetailView.as_view()),
    path('student/video/list/', StudentVideoListView.as_view()),
    path('remove/student/video/action/', RemoveAllStudentVideoActionsView.as_view()),

    # path('fetch/trial/test/', InsertTrialTests.as_view()),
    # path('fetch/topic/quiz/', FetchTopicQuiz.as_view()),
    # path('student/visit/clear/', RemoveUnnecessaryStudentVisitView.as_view()),
]
