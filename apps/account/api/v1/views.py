import random

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status, permissions, filters
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.account.models import Account, VerifyPhoneNumber, Country
from .permissions import IsOwnUserOrReadOnly
from .serializers import RegisterSerializer, LoginSerializer, VerifyPhoneNumberRegisterSerializer, \
    VerifyPhoneNumberSerializer, ChangePasswordSerializer, AccountProfileSerializer, AboutMeSerializer, \
    MyCompetitionsHistorySerializer, CountrySerializer
from rest_framework.response import Response

from .utils import verify


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            phone_number = serializer.data['phone_number']
            code = str(random.randint(100_000, 999_999))
            # verify(phone_number, code)  # sms provider kelganida ishga tushadi
            VerifyPhoneNumber.objects.create(phone_number=phone_number, code=code)
            data = {
                'code': code
            }
            return Response({'success': True, 'message': 'Please verify phone number', 'data': data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': f'{e}'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            phone_number = user_data['phone_number']
            user = Account.objects.get(phone_number=phone_number)
            code = str(random.randint(100_000, 999_999))
            if VerifyPhoneNumber.objects.filter(phone_number=phone_number).first():
                check = VerifyPhoneNumber.objects.get(phone_number=phone_number)
                check.delete()
            if len(phone_number) == 13:
                # verify(phone_number, code) sms provider kelganda ishlaydi
                VerifyPhoneNumber.objects.create(phone_number=phone_number, code=code)
            if verify:
                return Response({
                    'success': True, 'message': 'Verification code was sent to your phon number', 'code': code,
                    'tokens': user.tokens
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'err': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneNumberAPIView(generics.GenericAPIView):
    serializer_class = VerifyPhoneNumberSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        verify_code = VerifyPhoneNumber.objects.filter(phone_number=phone_number, code=code).first()
        if verify_code:
            user = Account.objects.filter(phone_number=phone_number).first()
            user.is_verified = True
            user.save()
            verify_code.delete()
            return Response({
                'status': True,
                'message': 'Phone number is verified'
            }, status=status.HTTP_200_OK)
        return Response({'message': 'Phone number or code invalid'}, status=status.HTTP_400_BAD_REQUEST)


class ReVerifyPhoneNumberAPIView(generics.GenericAPIView):
    serializer_class = VerifyPhoneNumberRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            phone_number = request.data.get('phone_number')
            code = str(random.randint(100_000, 999_999))
            verify_code = VerifyPhoneNumber.objects.get(phone_number=phone_number)
            if verify_code:
                verify_code.code = code
                verify_code.save()
                # verify(phone_number, code)

            data = {
                'code': code
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(generics.GenericAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            user = self.request.user
            user.is_verified = False
            user.save()
            refresh = user.tokens['refresh']
            access = user.tokens['access']
            refresh.blacklist()
            access.blacklist()
            return Response({
                "message": "Logout Success"
            }, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordCompletedView(generics.UpdateAPIView):
    # http://127.0.0.1:8000/account/change-password/
    queryset = Account.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsOwnUserOrReadOnly,)
    # parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'phone_number'

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)


class UserProfileListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountProfileSerializer


class PersonalUserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountProfileSerializer
    permission_classes = (IsOwnUserOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'phone_number'


class AboutMeListView(generics.RetrieveAPIView):
    queryset = Account.objects.filter(is_verified=True)
    permission_classes = (IsOwnUserOrReadOnly,)
    serializer_class = AboutMeSerializer
    lookup_field = 'phone_number'


@api_view(['GET'])
@permission_classes([IsOwnUserOrReadOnly])
def me(request):
    user = request.user
    qs = get_object_or_404(Account, id=user.id, is_verified=True)
    sz = AboutMeSerializer(qs)
    return Response(sz.data)


class MyCompetitionsHistoryListView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = MyCompetitionsHistorySerializer
    permission_classes = (IsOwnUserOrReadOnly,)
    lookup_field = 'pk'




class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    search_fields = ['name']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
