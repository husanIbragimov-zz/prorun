from import_export import resources
from import_export.fields import Field
from .models import Participant
from django.shortcuts import get_object_or_404
from datetime import timedelta


class ParticipantResource(resources.ModelResource):
    bib = Field(attribute='personal_id', column_name='Bib')
    tag = Field(attribute='tag', column_name='Tag')
    position = Field(attribute='position', column_name='Position')
    time = Field(attribute='duration', column_name='Time')
    distance = Field(attribute='distance', column_name='Distance')
    name = Field(attribute='user__first_name', column_name='Name')
    surname = Field(attribute='user__last_name', column_name='Surname')
    birthday = Field(attribute='user__birthday', column_name='Birthday')
    gender = Field(attribute='user__gender', column_name='Gender')
    country = Field(attribute='user__country__name', column_name='Country')
    city = Field(attribute='user__city__name', column_name='City')
    size = Field(attribute='user__size', column_name='Size')
    id = Field(attribute='user_id', column_name='ID')

    class Meta:
        model = Participant
        fields = (
            'bib', 'tag', 'position', 'time', 'distance', 'name', 'surname', 'birthday', 'gender', 'country',
            'city', 'size', 'id')

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        Manually removing commit hooks for intermediate save_points of atomic transaction
        """

        for data in dataset:
            model = get_object_or_404(Participant, id=data[12])
            duration_str = data[4]
            position_str = data[2]
            try:

                position_numeric = float(position_str)
                model.position = position_numeric
                model.personal_id = data[0]
                model.duration = timedelta(seconds=float(duration_str))
            except ValueError:
                pass

            model.save()
