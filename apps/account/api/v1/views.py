import random

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import generics, status, permissions, filters, mixins, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from apps.account.models import Account, VerifyPhoneNumber, Country, SportClub, City
from .permissions import IsOwnUserOrReadOnly
from .serializers import RegisterSerializer, LoginSerializer, VerifyPhoneNumberRegisterSerializer, \
    VerifyPhoneNumberSerializer, ChangePasswordSerializer, AccountProfileSerializer, AboutMeSerializer, \
    MyCompetitionsHistorySerializer, CountrySerializer, CitySerializer, SetNewPasswordSerializer, SportClubSerializer
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
            response = verify(phone_number, code)
            if response.status_code == 200:  # sms provider kelganida ishga tushadi
                user = get_object_or_404(Account, phone_number=phone_number)
                user.code = code
                user.save()
                return Response({'success': True, 'message': 'Please verify phone number'},
                                status=status.HTTP_201_CREATED)
            if response.status_code == 401:
                return Response({'success': False, 'message': 'Invalid token, Please try again'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'success': False, 'message': f'{e}'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        phone_number = request.data.get('phone_number')
        user = get_object_or_404(Account, phone_number=phone_number)
        if user.is_verified:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid()
            return Response({
                'success': True, 'message': 'Verification code was sent to your phon number',
                'tokens': user.tokens
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False, 'message': 'User is not verified'
        }, status=status.HTTP_401_UNAUTHORIZED)


class VerifyPhoneNumberAPIView(generics.GenericAPIView):
    serializer_class = VerifyPhoneNumberSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        user = get_object_or_404(Account, phone_number=phone_number, code=code)
        if user:
            user.is_verified = True
            user.save()
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
            user = get_object_or_404(Account, phone_number=phone_number)
            if user:
                user.code = code
                user.save()
                verify(phone_number, code)

            return Response({"success": True, "message": "verify code sent your phone number"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, 'error': 'Something went wrong'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(generics.GenericAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            user = self.request.user
            refresh = user.tokens['refresh']
            access = user.tokens['access']
            refresh.blacklist()
            access.blacklist()
            user.save()
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


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountProfileSerializer
    permission_classes = (IsOwnUserOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'phone_number'

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        qs = get_object_or_404(Account, id=user.id, is_verified=True)
        sz = AccountProfileSerializer(qs)
        return Response(sz.data)


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
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    search_fields = ['name']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class CityListView(generics.ListCreateAPIView):
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search:
            return City.objects.filter(Q(country_id=search) | Q(name__icontains=search)).order_by('country__name')
        return City.objects.all().order_by('country__name')


class SportClubListView(generics.ListCreateAPIView):
    queryset = SportClub.objects.all().order_by('name')
    serializer_class = SportClubSerializer
    search_fields = ['name']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    parser_classes = (MultiPartParser, FormParser)


class SetNewPasswordCompletedAPIView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    # http://127.0.0.1:8000/account/api/v1/forgot-password/
    serializer_class = SetNewPasswordSerializer
    queryset = Account.objects.all()
    lookup_field = 'code'
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        code = self.kwargs['code']
        serializer = self.serializer_class(data=request.data, context={'request': request, 'code': code})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
