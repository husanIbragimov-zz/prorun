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
    competition = serializers.CharField(source='competition.title', read_only=True)

    class Meta:
        model = CompetitionDetail
        fields = ('id', 'competition', 'title', 'image', 'texts')


class CompetitionParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'get_fullname', 'avatar')


class CompetitionDetailChildren(serializers.ModelSerializer):
    class Meta:
        model = CompetitionDetail
        fields = ('id', 'title')

class CompetitionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    participants = serializers.SerializerMethodField()
    competition_details = serializers.SerializerMethodField()

    def get_competition_details(self, obj):
        qs = CompetitionDetail.objects.filter(competition_id=obj.id)
        sz = CompetitionDetailChildren(qs, many=True)
        return sz.data

    def get_participants(self, obj):
        user = Account.objects.filter(competitions__competition_detail__competition=obj).order_by('-id')[:3]
        sz = CompetitionParticipantsSerializer(user, many=True)
        return sz.data

    class Meta:
        model = Competition
        fields = (
            'id', 'category', 'title', 'image', 'distance', 'created_at', 'participants', 'competition_details'
        )


class ParticipantListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='participant.get_fullname', read_only=True)
    address = serializers.CharField(source='participant.address', read_only=True)
    flag = serializers.CharField(source='participant.address.flag', read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'full_name', 'address', 'flag', 'personal_id', 'duration')


class ParticipantDataSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='competition.title', read_only=True)
    participants = ParticipantListSerializer(many=True)

    class Meta:
        model = CompetitionDetail
        fields = ('id', 'title', 'participants')


class CompetitionDetailListSerializer(serializers.ModelSerializer):
    texts = TextDetailSerializer(many=True)
    competition = serializers.CharField(source='competition.title', read_only=True)
    participants = serializers.SerializerMethodField()
    period = serializers.CharField(source='competition.period', read_only=True)
    distance = serializers.CharField(source='competition.distance', read_only=True)
    members = serializers.CharField(source='competition.members', read_only=True)
    free_places = serializers.CharField(source='competition.free_places', read_only=True)
    limit = serializers.CharField(source='competition.limit', read_only=True)

    def get_participants(self, obj):
        user = Account.objects.filter(competitions__competition_detail=obj).order_by('-id')[:3]
        sz = CompetitionParticipantsSerializer(user, many=True)
        return sz.data

    class Meta:
        model = CompetitionDetail
        fields = (
            'id', 'competition', 'title', 'image', 'period', 'distance', 'members', 'free_places', 'limit',
            'participants', 'texts')


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


class CompetitionDetailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        pass
