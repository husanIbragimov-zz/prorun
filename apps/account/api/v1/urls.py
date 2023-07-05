from django.urls import path, include

from apps.account.api.v1.views import RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view())
]
