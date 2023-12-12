from django_filters import FilterSet, DateRangeFilter
from .models import Post


class PostFilter(FilterSet):
    time_to_update = DateRangeFilter()

    class Meta:
        model = Post
        fields = {'author': ['exact'],
                  'header': ['icontains'],
                  'rating': ['gte'],
                  'time_to_update': ['exact']}
