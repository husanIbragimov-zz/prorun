import random

from rest_framework.authtoken.models import Token
from rest_framework import generics, status, authentication, permissions
from rest_framework.permissions import IsAuthenticated

from apps.account.models import Account, VerifyPhoneNumber
from .permissions import IsOwnUserOrReadOnly
from .serializers import RegisterSerializer, LoginSerializer, VerifyPhoneNumberRegisterSerializer, \
    VerifyPhoneNumberSerializer, ChangePasswordSerializer
from rest_framework.response import Response

from .utils import verify


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            phone_number = serializer.data['phone_number']
            code = str(random.randint(100_000, 999_999))
            # verify(phone_number, code) sms provider kelganida ishga tushadi
            VerifyPhoneNumber.objects.create(phone_number=phone_number, code=code)
            data = {
                'code': code
            }
            return Response({'success': True, 'message': 'Please verify phone number', 'data': data},
                            status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': f'Error'},
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
            return Response({'err': f'{e}'})

