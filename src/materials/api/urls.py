from django.urls import path
from .views import SubjectListView, ChaptersAndTopicsListView, FullSubjectListView
# from .views import SetUnreachedMidCotrolTopicsView

# from .views import FetchExistingMaterials

urlpatterns = [
    path('subject/list/', SubjectListView.as_view()),
    path('chapter/topic/list/<subject_pk>/', ChaptersAndTopicsListView.as_view()),
    path('subject/full/list/', FullSubjectListView.as_view()),

    # path('topic/complement/quiz/', SetUnreachedMidCotrolTopicsView.as_view()),

    # path('fetch/', FetchExistingMaterials.as_view()),
]
