from django.urls import path, include

from apps.account.api.v1.views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]
