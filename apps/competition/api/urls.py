from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.competition.api.v1.urls'))
]
