from django.urls import path
from .views import (
    SubjectQuizConfigurationListView,
    LessonGroupIPConfigurationDetailView,
    ResetLessonGroupIpConfigurationView,
)

urlpatterns = [
    path('subject/quiz/list/', SubjectQuizConfigurationListView.as_view()),
    path('lesson/group/check/ip/get/', LessonGroupIPConfigurationDetailView.as_view()),
    path('lesson/group/check/ip/set/', LessonGroupIPConfigurationDetailView.as_view()),
    path('lesson/group/check/ip/unset/', LessonGroupIPConfigurationDetailView.as_view()),
    path('reset/material/ip/', ResetLessonGroupIpConfigurationView.as_view()),
]
