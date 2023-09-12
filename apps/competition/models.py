from django.db import models
from apps.account.models import Account
from apps.base.models import BaseModel
from datetime import datetime
from apps.main.models import Partner

STATUS = (
    ('future', 'Future'),
    ('now', 'Now'),
    ('past', 'Past')
)


class Category(BaseModel):
    title = models.CharField(max_length=223, null=True, blank=True)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    svg = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Competition(BaseModel):
    status = models.CharField(choices=STATUS, null=True, blank=True, max_length=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=223, null=True, blank=True)
    sub_title = models.CharField(max_length=223, null=True, blank=True)
    image = models.ImageField(upload_to='competitions/', null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    media = models.FileField(upload_to='video/', null=True, blank=True)
    period = models.CharField(max_length=223, null=True, blank=True)
    distance = models.CharField(max_length=223, null=True, blank=True)
    members = models.IntegerField(null=True, blank=True)
    where_is_ticket = models.URLField(null=True, blank=True)
    limit = models.CharField(max_length=223, null=True, blank=True)
    partners = models.ManyToManyField(Partner, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    def update_status(self):
        curr_date = datetime.now().date()
        if self.start_date > curr_date and self.end_date > curr_date:
            self.status = 'future'
        elif self.start_date <= curr_date and self.end_date >= curr_date:
            self.status = 'now'
        else:
            self.status = 'past'
        self.save()
        return "success"


class CompetitionMaps(BaseModel):
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="competition_maps")
    maps = models.ImageField(upload_to='maps/', null=True, blank=True)
    title = models.CharField(max_length=223, null=True, blank=True)

    @property
    def set_position(self):
        qs = self.participant_choices.filter(choice_id=self.id).order_by('duration')
        counter = 0
        for i in qs:
            counter += 1
            i.position = counter
            i.save()
        return qs

    def __str__(self):
        return self.title


class CompetitionTexts(BaseModel):
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="competition_texts")
    title = models.CharField(max_length=223, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Participant(BaseModel):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="competitions")
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="competition_participants")
    choice = models.ForeignKey(CompetitionMaps, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="participant_choices")
    distance = models.CharField(max_length=50, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    personal_id = models.CharField(max_length=223, null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_code/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_fullname}"
