from django.urls import path
from .views import NewsDefaultBannerListView, NewsRetrieveAPIView, NewsListView


urlpatterns = [
    path('banner/', NewsDefaultBannerListView.as_view()),
    path('news/', NewsListView.as_view()),
    path('news/<int:pk>/', NewsRetrieveAPIView.as_view()),
]
