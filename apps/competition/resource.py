from import_export import resources
from import_export.fields import Field
from .models import Participant
from django.shortcuts import get_object_or_404
from datetime import timedelta


class ParticipantResource(resources.ModelResource):

    class Meta:
        model = Participant
        fields = ('id', 'position', 'user__first_name', 'competition__title', 'choice__title', 'personal_id', 'user__sport_club__name', 'duration', 'distance')

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        Manually removing commit hooks for intermediate savepoints of atomic transaction
        """
        print(result, dataset)
        
        for data in dataset:
            print(data)
            model = get_object_or_404(Participant, id=data[0])
            print(model)
            duration_str = data[7]
            position_str = data[2]
            try:
                    
                position_numeric = float(position_str)
                model.position = position_numeric
                model.personal_id = data[3]
                model.duration = timedelta(seconds=float(duration_str))
            except ValueError:
                pass
            
            model.save()