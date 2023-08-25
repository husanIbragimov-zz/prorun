from django.urls import path
from .views import CategoryListView, CompetitionFutureListView, CompetitionDetailListView, CompetitionPresentListView, \
    CompetitionPastListView, ParticipantCreateView, ParticipantListView, ParticipantRetrieveView, \
    CompetitionDetailRetrieveAPIView, ParticipantDataListView

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('competitions/future/', CompetitionFutureListView.as_view()),
    path('competitions/present/', CompetitionPresentListView.as_view()),
    path('competitions/past/', CompetitionPastListView.as_view()),
    # path('detail/', CompetitionDetailListView.as_view()),
    path('detail/<int:pk>/', CompetitionDetailRetrieveAPIView.as_view()),

    path('register/participant/', ParticipantCreateView.as_view()),
    path('participants/<int:pk>/', ParticipantDataListView.as_view())
]
