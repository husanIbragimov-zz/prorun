from django.urls import path
from .views import CategoryListView, BannerImagesListView, FutureCompetitionListView, PastCompetitionListView, \
    ParticipantRetrieveView, CompetitionDetailRetrieveAPIView, JoinToCompetitionCreateView, MyCompetitionGetListView, \
    MyOldCompetitionsListView, ParticipantQRCodeView

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('competitions/future/', FutureCompetitionListView.as_view()),
    path('competitions/present/', BannerImagesListView.as_view()),
    path('competitions/past/', PastCompetitionListView.as_view()),
    path('participant/<int:choice_id>/', ParticipantRetrieveView.as_view()),
    path('detail/<int:pk>/', CompetitionDetailRetrieveAPIView.as_view()),
    path('join/<int:choice_id>/', JoinToCompetitionCreateView.as_view()),
    path('my-competitions/', MyCompetitionGetListView.as_view()),
    path('my-old-competitions/', MyOldCompetitionsListView.as_view()),

    path('participant/qrcode/<int:competition_id>/', ParticipantQRCodeView.as_view(), name='user_qrcode'),
]
