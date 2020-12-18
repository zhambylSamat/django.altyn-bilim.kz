from django.urls import path
from .views import CalculateSalaryListView, GroupListForSalaryCalculations
# from .views import TmpSetTeacherSalaryCoefficientView

urlpatterns = [
    path('salary/<month>/<year>/<lesson_group_id>/', CalculateSalaryListView.as_view()),
    path('calculation/group/list/<month>/<year>/', GroupListForSalaryCalculations.as_view()),

    # path('salary/coefficient/<teacher_salary_category_pk>/', TmpSetTeacherSalaryCoefficientView.as_view()),
]
