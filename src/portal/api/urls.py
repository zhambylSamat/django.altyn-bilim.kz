from django.urls import path
from .views import (
    StaffAuthView,
    RoleListView,
    StaffChangePasswordView,
    TeacherAuthView,
    StudentAuthView,
    StudentChangePasswordView,
    RequestFromClientView,
)

urlpatterns = [
    path('token/staff/', StaffAuthView.as_view()),
    path('token/teacher/', TeacherAuthView.as_view()),
    path('token/student/', StudentAuthView.as_view()),
    path('role/list/', RoleListView.as_view()),
    path('change/password/staff/', StaffChangePasswordView.as_view()),
    path('change/password/student/', StudentChangePasswordView.as_view()),
    path('send/request/from/client/', RequestFromClientView.as_view()),
]