from rest_framework import serializers
from apps.competition.models import Category, Competition, CompetitionDetail, Participant, TextDetail


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'icon')


class TextDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextDetail
        fields = ('id', 'title', 'description')


class CompetitionDetailSerializer(serializers.ModelSerializer):
    texts = TextDetailSerializer(many=True)
    competition = serializers.CharField(source='competition.title')

    class Meta:
        model = CompetitionDetail
        fields = ('id', 'competition', 'title', 'image', 'texts')


class CompetitionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Competition
        fields = (
            'id', 'category', 'title', 'image', 'created_at'
        )


class ParticipantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'participant', 'duration', 'overrun', 'personal_id', 'created_at')


class CompetitionDetailListSerializer(serializers.ModelSerializer):
    texts = TextDetailSerializer(many=True)
    competition = serializers.CharField(source='competition.title')
    participants = ParticipantListSerializer(many=True)

    class Meta:
        model = CompetitionDetail
        fields = ('id', 'competition', 'title', 'youtube', 'media', 'image', 'participants', 'texts')


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'competition_detail', 'participant')


class UserCompetitionsSerializer(serializers.ModelSerializer):
    competition_detail = serializers.CharField(source='competition_detail.title', read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'competition_detail', 'duration', 'overrun', 'personal_id', 'created_at')
