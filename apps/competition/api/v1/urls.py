from django.urls import path
# from .views import CategoryListView, CompetitionFutureListView, CompetitionPresentListView, \
#     ParticipantListView, ParticipantRetrieveView, CompetitionCategoryRetrieveView, \
#     CompetitionCategoryListView

from .viewss import CategoryListView, BannerImagesListView, FutureCompetitionListView, PastCompetitionListView, \
    ParticipantRetrieveView, CompetitionDetailRetrieveAPIView

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('competitions/future/', FutureCompetitionListView.as_view()),
    path('competitions/present/', BannerImagesListView.as_view()),
    path('competitions/past/', PastCompetitionListView.as_view()),
    path('participant/<int:choice_id>/', ParticipantRetrieveView.as_view()),
    path('detail/<int:pk>/', CompetitionDetailRetrieveAPIView.as_view()),
    # path('detail/', CompetitionDetailListView.as_view()),
    # path('detail/<int:pk>/', CompetitionDetailRetrieveAPIView.as_view()),

    # path('register/participant/', ParticipantCreateView.as_view()),
    # path('participants/<int:pk>/', ParticipantDataListView.as_view()),
    # path('competition_category/<int:pk>/', CompetitionCategoryRetrieveView.as_view()),
    # path('competition_category/', CompetitionCategoryListView.as_view()),
]
