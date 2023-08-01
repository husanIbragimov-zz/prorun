import requests


def verify(phone_number, code):
    URL = ""
    PARAMS = {
        "Authorization": ""
    }
    phone_number = str(phone_number)[1:13]
    data = {
        'phone_number': phone_number,
        'verify_code': code,
        'from': '',
        'callback_url': ''
    }

    response = requests.request('POST', URL, data=data, headers=PARAMS)
    print(response.json())
    return response
