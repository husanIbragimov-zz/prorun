from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.account.models import Account, VerifyPhoneNumber


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=16, write_only=True)

    class Meta:
        model = Account
        fields = ('id', 'phone_number', 'password', 'avatar', 'first_name', 'last_name', 'gender', 'birthday', 'tokens')

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

