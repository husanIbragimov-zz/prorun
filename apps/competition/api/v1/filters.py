import django_filters
from django.db.models import Q
from apps.competition.models import Competition, Category


class BannerCompetitionFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr='icontains')
    category = django_filters.CharFilter(field_name="category__title", lookup_expr='icontains')
    category_id = django_filters.NumberFilter(field_name="category_id", lookup_expr='exact')

    class Meta:
        model = Competition
        fields = ('title', 'category', 'category_id')
