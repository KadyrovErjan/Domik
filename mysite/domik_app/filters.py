from .models import House
from django_filters import FilterSet


class HouseFilter(FilterSet):
    class Meta:
        model = House
        fields = {
            'category': ['exact'],
            'area': ['gt', 'lt'],
            'entry': ['gt', 'lt'],
            'departure': ['gt', 'lt'],
            'floor': ['gt', 'lt'],
            'plot': ['gt', 'lt'],
            'count_people': ['gt', 'lt'],
            'weekdays_price': ['gt', 'lt']
        }