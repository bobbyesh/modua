# filters.py

from rest_framework import filters
import django_filters
from .models import Word, Definition

class WordFilter(filters.FilterSet):
    username = django_filters.CharFilter(name='user__username')
    language = django_filters.CharFilter(name='language', lookup_expr='language')
    article = django_filters.NumberFilter(name='articles__id')

    class Meta:
        model = Word
        fields = ['word', 'language', 'username', 'ease', 'article']


class DefinitionFilter(filters.FilterSet):
    word = django_filters.CharFilter(name='word__word')
    username = django_filters.CharFilter(name='word__user__username')
    language = django_filters.CharFilter(name='word__language__language')
    target = django_filters.CharFilter(name='language__language')

    class Meta:
        model = Definition
        fields = ['word', 'language', 'username', 'definition', 'target']
