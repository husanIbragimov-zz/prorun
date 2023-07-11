from django.urls import path
from .views import CategoryListView, CompetitionFutureListView, CompetitionDetailListView, CompetitionPresentListView, \
    CompetitionPastListView

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('competitions/future/', CompetitionFutureListView.as_view()),
    path('competitions/present/', CompetitionPresentListView.as_view()),
    path('competitions/past/', CompetitionPastListView.as_view()),
    path('detail/', CompetitionDetailListView.as_view()),
]
