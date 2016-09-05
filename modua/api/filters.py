# filters.py

import django_filters
from .models import Word

class WordFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name='user__username')
    language = django_filters.CharFilter(name='language', lookup_expr='language')
    article = django_filters.NumberFilter(name='articles__id')

    class Meta:
        model = Word
        fields = ['word', 'language', 'username', 'ease', 'article']
        together = ['word', 'language']
