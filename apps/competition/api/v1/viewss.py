from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response

from apps.competition.models import Category, Competition, CompetitionMaps, Participant

from .serializerss import CategorySerializer, BannerImagesSerializer, FutureCompetitionSerializer, \
    PastCompetitionSerializer, CompetitionDetailSerializer, JoinToCompetitionCreateSerializer, \
    CompetitionMapsUserListSerializer

from .filters import BannerCompetitionFilter


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class BannerImagesListView(generics.ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = BannerImagesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category__title', 'category_id']
    filterset_class = BannerCompetitionFilter

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(Q(status='now')).order_by('-id')
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class FutureCompetitionListView(generics.ListAPIView):
    queryset = Competition.objects.filter(status='future').order_by('-id')
    serializer_class = FutureCompetitionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category__title', 'category_id']
    filterset_class = BannerCompetitionFilter


class PastCompetitionListView(generics.ListAPIView):
    queryset = Competition.objects.filter(status='past').order_by('-id')[0:3]
    serializer_class = PastCompetitionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category__title', 'category_id']
    filterset_class = BannerCompetitionFilter


class ParticipantRetrieveView(generics.ListAPIView):
    queryset = CompetitionMaps.objects.all()
    serializer_class = CompetitionMapsUserListSerializer
    lookup_field = 'choice_id'

    def get_queryset(self):
        choice_id = self.kwargs['choice_id']
        return self.queryset.filter(Q(competition_id=choice_id))


class CompetitionDetailRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionDetailSerializer
    lookup_field = 'pk'


class JoinToCompetitionCreateView(generics.CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = JoinToCompetitionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        competition_map_id = self.kwargs['choice_id']
        user = self.request.user
        competition_map = get_object_or_404(CompetitionMaps, id=competition_map_id)
        competition = get_object_or_404(Competition, id=competition_map.competition.id)
        if competition_map.participant_choices.filter(user=user):
            return Response({"message": "You have already joined this competition"}, status=status.HTTP_400_BAD_REQUEST)

        if competition_map and competition.status == 'now':
            Participant.objects.get_or_create(user=user, choice_id=competition_map.id, competition_id=competition.id)
            return Response({'message': 'Success'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
