from django.db import models
from apps.account.models import Account
from apps.base.models import BaseModel
from datetime import datetime

STATUS = (
    ('future', 'Future'),
    ('now', 'Now'),
    ('past', 'Past')
)


class Category(BaseModel):
    title = models.CharField(max_length=223, null=True, blank=True)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Competition(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=223, null=True, blank=True)
    image = models.ImageField(upload_to='competitions/', null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    distance = models.CharField(max_length=223, null=True, blank=True)
    status = models.CharField(choices=STATUS, null=True, blank=True, max_length=6)
    period = models.CharField(max_length=223, null=True, blank=True)
    members = models.IntegerField(null=True, blank=True)
    free_places = models.CharField(max_length=223, null=True, blank=True)
    time_limit = models.CharField(max_length=223, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    def get_period(self):
        curr_date = datetime.now().date()
        if self.start_date > curr_date and self.end_date > curr_date:
            self.status = 'future'

        elif self.start_date <= curr_date and self.end_date >= curr_date:
            self.status = 'now'

        else:
            self.status = 'past'
        self.save()
        return "success"


class CompetitionDetail(BaseModel):
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='competition_details')
    title = models.CharField(max_length=223, null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    media = models.FileField(upload_to='video/', null=True, blank=True)
    image = models.ImageField(upload_to='maps/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.title:
            return f"{self.title}"
        return 'No title'


class Participant(BaseModel):
    competition_detail = models.ForeignKey(CompetitionDetail, on_delete=models.SET_NULL, null=True,
                                           related_name='participants')
    participant = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='competitions')
    duration = models.CharField(max_length=223, null=True, blank=True)
    overrun = models.FloatField(null=True, blank=True)
    personal_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.duration}"


class TextDetail(BaseModel):
    competition_detail = models.ForeignKey(CompetitionDetail, on_delete=models.SET_NULL, null=True,
                                           related_name='texts')
    title = models.CharField(max_length=223, null=True, blank=True)
    description = models.CharField(max_length=550, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
