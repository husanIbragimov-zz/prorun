from rest_framework import generics

from apps.main.api.v1.serializers import NewsDefaultSerializer, NewsSerializer
from apps.main.models import News


class NewsDefaultBannerListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDefaultSerializer


class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsRetrieveAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'pk'
