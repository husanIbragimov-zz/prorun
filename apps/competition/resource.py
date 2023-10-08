from import_export import resources
from import_export.fields import Field
from .models import Participant
from django.shortcuts import get_object_or_404


class ParticipantResource(resources.ModelResource):

    class Meta:
        model = Participant
        fields = ('id', 'position', 'user__first_name', 'competition__title', 'choice__title', 'personal_id', 'user__sport_club__name', 'duration', 'distance')

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        Manually removing commit hooks for intermediate savepoints of atomic transaction
        """
        print(dataset)
        
        for data in dataset:
            print(data)
            model = get_object_or_404(Participant, id=data[0])
            model.position = data[1] if data[1] else None
            model.personal_id = data[4] if data[4] else None
            model.duration = data[7] if data[7] else None
            model.save()