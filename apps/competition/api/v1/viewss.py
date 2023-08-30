from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from apps.competition.models import Category, Competition, CompetitionTexts, CompetitionMaps, Participant

from .serializerss import CategorySerializer, BannerImagesSerializer, FutureCompetitionSerializer, \
    PastCompetitionSerializer, ParticipantListSerializer, CompetitionDetailSerializer, \
    JoinToCompetitionCreateSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class BannerImagesListView(generics.ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = BannerImagesSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(Q(status='now')).order_by('-id')
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class FutureCompetitionListView(generics.ListAPIView):
    queryset = Competition.objects.filter(status='future').order_by('-id')
    serializer_class = FutureCompetitionSerializer


class PastCompetitionListView(generics.ListAPIView):
    queryset = Competition.objects.filter(status='past').order_by('-id')[0:3]
    serializer_class = PastCompetitionSerializer


class ParticipantRetrieveView(generics.ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantListSerializer
    lookup_field = 'choice_id'

    def get_queryset(self):
        choice_id = self.kwargs['choice_id']
        return self.queryset.filter(Q(choice_id=choice_id)).order_by('duration')


class CompetitionDetailRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionDetailSerializer
    lookup_field = 'pk'


class JoinToCompetitionCreateView(generics.CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = JoinToCompetitionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'competition_detail'

    def post(self, request, *args, **kwargs):
        competition_map_id = self.kwargs['choice_id']
        user = self.request.user
        competition_map = get_object_or_404(CompetitionMaps, id=competition_map_id, status='future')
        if competition_map.participant_choices.filter(user=user).exists():
            return Response({"message": "You have already joined this competition"}, status=status.HTTP_400_BAD_REQUEST)

        if competition_map:
            sz = self.serializer_class(data=request.data)
            if sz.is_valid():
                sz.save(user=user, choice_id=competition_map, cometition_id=competition_map.competition.id)
                return Response({'message': 'Success'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
