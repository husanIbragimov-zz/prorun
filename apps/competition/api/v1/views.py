from django.db.models import Q
from rest_framework import generics, status
from apps.competition.models import Category, Competition, CompetitionDetail, Participant
from .serializers import CategorySerializer, CompetitionSerializer, CompetitionDetailSerializer, ParticipantSerializer, \
    CompetitionDetailListSerializer, ParticipantListSerializer, ParticipantDataSerializer
from django.utils import timezone
from rest_framework.response import Response


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CompetitionFutureListView(generics.ListAPIView):
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        queryset = Competition.objects.filter(status='future').order_by('-id')
        return queryset


class CompetitionPresentListView(generics.ListAPIView):
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        queryset = Competition.objects.filter(status='now').order_by('-id')
        return queryset


class CompetitionPastListView(generics.ListAPIView):
    serializer_class = ParticipantDataSerializer

    def get_queryset(self):
        queryset = CompetitionDetail.objects.filter(competition__status='past').order_by('-id')
        return queryset


class CompetitionDetailListView(generics.ListAPIView):
    queryset = CompetitionDetail.objects.all()
    serializer_class = CompetitionDetailListSerializer


class CompetitionDetailRetrieveAPIView(generics.RetrieveAPIView):
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


class ParticipantDataListView(generics.RetrieveAPIView):
    queryset = CompetitionDetail.objects.all()
    serializer_class = ParticipantDataSerializer
    lookup_field = 'pk'
