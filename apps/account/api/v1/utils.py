import os
import requests
from django.conf import settings
from apps.account.models import SMSToken

EMAIL = settings.EMAIL
PASSWORD = settings.PASSWORD


def login(email, password):
    URL = "https://notify.eskiz.uz/api/auth/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.request('POST', URL, data=data)
    SMSToken.objects.create(token=response.json()['data']['token'])
    return response


def verify(phone_number, code):
    token = SMSToken.objects.last().token
    phone_number = str(phone_number)[1:13]
    URL = "https://notify.eskiz.uz/api/message/sms/send"
    PARAMS = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        'mobile_phone': phone_number,
        'message': f"Verify code: {code}",
        'from': '4546',
        'callback_url': 'http://0000.uz/test.php'
    }
    response = requests.request('POST', URL, data=data, headers=PARAMS)
    if response.status_code == 401:
        login(EMAIL, PASSWORD)
        verify(phone_number, code)
    return response
