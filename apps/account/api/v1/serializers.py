from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.account.models import Account, VerifyPhoneNumber


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=16, write_only=True)

    class Meta:
        model = Account
        fields = ('id', 'phone_number', 'password', 'avatar', 'first_name', 'last_name', 'gender', 'birthday')

