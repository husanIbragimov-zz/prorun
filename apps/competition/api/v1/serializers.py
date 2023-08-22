from rest_framework import serializers

from apps.account.models import Account
from apps.competition.models import Category, Competition, CompetitionDetail, Participant, TextDetail
from django.shortcuts import get_object_or_404


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


class CompetitionParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'get_fullname', 'avatar')


class CompetitionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    participants = serializers.SerializerMethodField()

    def get_participants(self, obj):
        user = Account.objects.filter(competitions__competition_detail__competition=obj).order_by('-id')[:3]
        sz = CompetitionParticipantsSerializer(user, many=True)
        return sz.data

    class Meta:
        model = Competition
        fields = (
            'id', 'category', 'title', 'image', 'created_at', 'participants'
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
        fields = ('id', 'competition', 'title', 'image', 'participants', 'texts')


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'competition_detail', 'participant')


class UserCompetitionsSerializer(serializers.ModelSerializer):
    competition_detail = serializers.CharField(source='competition_detail.title', read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'competition_detail', 'duration', 'overrun', 'personal_id', 'created_at')


class CompetitionDetailAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionDetail
        fields = ('id', 'competition', 'title', 'image')
