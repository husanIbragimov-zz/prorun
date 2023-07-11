from rest_framework import generics
from apps.competition.models import Category, Competition, CompetitionDetail, Participant
from .serializers import CategorySerializer, CompetitionSerializer, CompetitionDetailSerializer
from django.utils import timezone
from rest_framework.response import Response


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CompetitionFutureListView(generics.ListAPIView):
    queryset = Competition.objects.filter(status='future')
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        try:
            present = self.queryset.all()
            now = timezone.now() + timezone.timedelta(hours=5)
            print(now.replace(tzinfo=timezone.utc))
            for index in present:
                if index.start_date < now:
                    index.status = 'past'
                    index.save()
            return present.all()
        except Exception as e:
            return Response({'err': f'{e}'})


class CompetitionPresentListView(generics.ListAPIView):
    queryset = Competition.objects.filter(status='now')
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        try:
            present = self.queryset.all()
            now = timezone.now() + timezone.timedelta(hours=5)
            print(now.replace(tzinfo=timezone.utc))
            for index in present:
                if index.start_date < now:
                    index.status = 'past'
                    index.save()
            return present.all()
        except Exception as e:
            return Response({'err': f'{e}'})


class CompetitionPastListView(generics.ListAPIView):
    queryset = Competition.objects.filter(status='past')
    serializer_class = CompetitionSerializer



class CompetitionDetailListView(generics.ListAPIView):
    queryset = CompetitionDetail.objects.all()
    serializer_class = CompetitionDetailSerializer
