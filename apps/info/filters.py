import django_filters.rest_framework as filters

from apps.info.models import FAQ


class FAQFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='question', lookup_expr='icontains')
    category_id = filters.NumberFilter(field_name='category__id', lookup_expr='exact')

    class Meta:
        model = FAQ
        fields = ['search', 'category_id']
