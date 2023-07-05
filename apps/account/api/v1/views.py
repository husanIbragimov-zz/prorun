import random
from rest_framework import generics, status, authentication, permissions
from apps.account.models import Account, VerifyPhoneNumber
from .serializers import RegisterSerializer
from rest_framework.response import Response

from .utils import verify


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = Account.objects.filter(phone_number=request.data['phone_number'])
        if user:
            return Response({'message': 'User already exists'}, status=status.HTTP_409_CONFLICT)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data['phone_number']
        code = str(random.randint(100_000, 999_999))
        if len(phone_number) == 17:
            verify(phone_number, code)
            VerifyPhoneNumber.objects.create(phone_number=phone_number, code=code)
        data = {
            'code': code
        }

        return Response({'success': True, 'message': 'Please verify phone number', 'data': data},
                        status=status.HTTP_201_CREATED)
