import django_filters
from django.db.models import Q
from apps.competition.models import Competition, Category


class BannerCompetitionFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.CharFilter(method='filter_category')

    def filter_category(self, queryset, name, value):
        return queryset.filter(Q(category__title__icontains=value) | Q(category_id=value))

    class Meta:
        model = Competition
        fields = ('category',)
