from django.urls import path
from .views import (
    ResetStudentPasswordView,
    StudentNoPaymentStatusView
)

urlpatterns = [
    path('reset/student/<user_pk>/', ResetStudentPasswordView.as_view()),
    path('no_payment/<user_pk>/', StudentNoPaymentStatusView.as_view()),
    # path('student/list/', ListStudentView.as_view()),
]
