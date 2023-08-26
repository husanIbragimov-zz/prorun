from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.account.models import Account, VerifyPhoneNumber, phone_regex, Country
from apps.competition.api.v1.serializers import UserCompetitionsSerializer, CompetitionDetailAccountSerializer
from apps.competition.models import CompetitionDetail, Participant


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=16, write_only=True)
    # phone_number = serializers.CharField(max_length=17, validators=[phone_regex], write_only=True)
    avatar = serializers.ImageField()

    class Meta:
        model = Account
        fields = ('id', 'phone_number', 'password', 'first_name', 'last_name', 'avatar', 'gender', 'birthday')

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=13, required=True)
    password = serializers.CharField(max_length=16, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        user = Account.objects.filter(phone_number=obj.get('phone_number')).first()
        return user.tokens

    class Meta:
        model = Account
        fields = ('id', 'phone_number', 'password', 'tokens')

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError({'success': False, 'message': 'User not found'})
        if not user.is_verified:
            raise serializers.ValidationError({'success': False, 'message': 'User is not verified'})

        data = {
            'success': True,
            'phone_number': user.phone_number,
            'tokens': user.tokens
        }

        return data


class VerifyPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyPhoneNumber
        fields = '__all__'


class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=17)
    code = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=16)


class VerifyPhoneNumberRegisterSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VerifyPhoneNumber
        fields = ('phone_number', 'code')


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)

    class Meta:
        model = Account
        fields = ('password', 'old_password')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        request = self.context.get('request')
        user = request.user

        if not user.check_password(old_password):
            raise serializers.ValidationError({'success': False, 'message': 'Old password not match'})

        user.set_password(password)
        user.save()
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 'avatar', 'gender', 'birthday', 'address', 'tall',
            'weight', 'date_login', 'date_created'
        ]


class AboutMeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    phone_number = serializers.CharField()
    avatar = serializers.ImageField()

    class Meta:
        model = Account
        fields = ['id', 'phone_number', 'get_fullname', 'avatar']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'flag')


class ParticipantUserSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='competition_detail.competition.title', read_only=True)
    category_name = serializers.CharField(source='competition_detail.title', read_only=True)
    category_icon = serializers.ImageField(source='competition_detail.competition.category.icon', read_only=True)
    image = serializers.ImageField(source='competition_detail.image', read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'title', 'category_name', 'category_icon', 'image', 'duration', 'created_at')


class MyCompetitionsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_fullname', read_only=True)
    competitions = ParticipantUserSerializer(many=True)
    address = CountrySerializer(many=False)

    class Meta:
        model = Account
        fields = ('id', 'full_name', 'avatar', 'address', 'age', 'competitions')
