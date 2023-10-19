import requests
from django.conf import settings

TOKEN = settings.TOKEN

def verify(phone_number, code):
    URL = "https://notify.eskiz.uz/api/message/sms/send"
    PARAMS = {
        "Authorization": f"Bearer {TOKEN}"
    }
    phone_number = str(phone_number)[1:13]
    data = {
        'mobile_phone': phone_number,
        'message': f"Verify code: {code}",
        'from': 'prorun.uz',
        'callback_url': 'http://0000.uz/test.php'
    }

    response = requests.request('POST', URL, data=data, headers=PARAMS)
    # print(response.json())
    return response
