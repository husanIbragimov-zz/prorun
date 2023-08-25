import pandas as pd
import requests
from apps.account.models import Country


def get_country():
    url = "https://restcountries.com/v3.1/all"

    r = requests.get(url).json()

    df = pd.DataFrame(r)
    name = df['name']
    flag = df['flags']
    try:
        for i in range(len(name)):
            country = Country.objects.create(name=name[i].get('common'), flag=flag[i].get('png'))
            country.save()
        return 'zor'
    except Exception as e:
        return e
