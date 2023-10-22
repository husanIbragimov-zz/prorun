import pandas as pd
import requests
from apps.account.models import Country, City


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


def get_city():
    url = "https://gist.githubusercontent.com/ans2human/89f78752e161219060257b160f970fcd/raw/50d755da33db30ecb533d1770d94f9adcc8d6892/world_cities.json"

    r = requests.get(url).json()
    df = pd.DataFrame(r)
    admin_name = df['admin_name']
    country = df['country']
    print(len(admin_name))
    try:
        for i in range(len(admin_name)):
            countries = Country.objects.filter(name__icontains=country[i])
            if countries.exists():
                # You can choose one of the matching countries or implement custom logic.
                # For example, we choose the first matching country here.
                country_obj = countries.first()
            else:
                # If no matching country found, create a new one.
                country_obj = Country.objects.create(name=country[i])
            city, created = City.objects.get_or_create(name=admin_name[i], country=country_obj)
            city.save()
        return 'zor'
    except Exception as e:
        return str(e)
