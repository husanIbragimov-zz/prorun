from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Count
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.api.v1.serializers import CompetitionResultSerializer

phone_regex = RegexValidator(
    regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
    message="Phone number must be entered in the format: '+998 33 215 05 48'. Up to 13 digits allowed."
)


class AccountManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise TypeError('Invalid phone number')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        if not password:
            raise TypeError('password did not come!')
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_verified = True
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


GENDER = (
    ('none', 'None'),
    ('male', 'Male'),
    ('female', 'Female'),
)


class Country(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    flag = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class SportClub(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    flag = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=223, null=True, blank=True)
    last_name = models.CharField(max_length=223, null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                    unique=True, help_text='for example: +998945588859')  # validators should be a list
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER, default='none', help_text='none, male, female', null=True)
    birthday = models.DateField(null=True, blank=True)
    tall = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    address = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    sport_club = models.ForeignKey(SportClub, on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_login = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    # def get_monthly_results(self):
    #     # Assuming you have a related name 'participants' for the Participant model
    #     monthly_results = self.competitions.values('created_at__month', 'created_at__year').annotate(
    #         total_results=Count('id')
    #     )
    #
    #     data = []
    #     for result in monthly_results:
    #         month = result['created_at__month']
    #         year = result['created_at__year']
    #         results = self.competitions.filter(
    #             created_at__month=month,
    #             created_at__year=year
    #         )
    #         data.append({
    #             'month': f"{month}-{year}",
    #             'results': CompetitionResultSerializer(results, many=True).data
    #         })
    #
    #     return data

    def get_fullname(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name}'

    def age(self):
        curr = datetime.now().year
        if self.birthday:
            age = curr - self.birthday.year
            return age
        return 'no born year'

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data

    def __str__(self):
        return self.phone_number


class VerifyPhoneNumber(models.Model):
    class Meta:
        verbose_name = "Confirm phone number"
        verbose_name_plural = "Confirm phone number"

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                    unique=True, verbose_name="Phone number",
                                    help_text='for example: +998945588859')  # validators should be a list
    code = models.CharField(max_length=6, verbose_name="Code")

    def __str__(self):
        return f'📞 Phone number: {self.phone_number};  🔐 code: {self.code}'
