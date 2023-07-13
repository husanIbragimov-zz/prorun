from django.db.models import Q
from rest_framework import generics, status
from apps.competition.models import Category, Competition, CompetitionDetail, Participant
from .serializers import CategorySerializer, CompetitionSerializer, CompetitionDetailSerializer, ParticipantSerializer, \
    CompetitionDetailListSerializer, ParticipantListSerializer
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
                if index.start_date.date() == now.date():
                    index.status = 'now'
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
                if index.start_date.date() < now.date():
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
    serializer_class = CompetitionDetailListSerializer


class CompetitionDetailView(generics.RetrieveAPIView):
    queryset = CompetitionDetail.objects.all()
    serializer_class = CompetitionDetailListSerializer
    lookup_field = 'pk'


class ParticipantCreateView(generics.GenericAPIView):
    serializer_class = ParticipantSerializer

    # permission_classes = ()
    def post(self, request):
        user = request.user
        competition = request.data.get('competition_detail')
        if CompetitionDetail.objects.filter(Q(competition=competition) & Q(competition__status='future')):
            Participant.objects.create(competition=competition, participant=user)
        return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


class ParticipantListView(generics.ListAPIView):
    queryset = Participant.objects.filter(is_active=True)
    serializer_class = ParticipantListSerializer


class ParticipantRetrieveView(generics.RetrieveAPIView):
    queryset = Participant.objects.filter(is_active=True)
    serializer_class = ParticipantListSerializer
    lookup_field = 'pk'
