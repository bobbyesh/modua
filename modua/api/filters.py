# filters.py

from rest_framework import filters
import django_filters
from .models import Word, Definition


class WordFilter(filters.FilterSet):
    username = django_filters.CharFilter(name='owner__username')
    language = django_filters.CharFilter(name='language', lookup_expr='language')
    article = django_filters.NumberFilter(name='articles__id')

    class Meta:
        model = Word
        fields = ['word', 'language', 'username', 'ease', 'article', 'id']


class DefinitionFilter(filters.FilterSet):
    word = django_filters.CharFilter(name='word__word')
    username = django_filters.CharFilter(name='owner__username')
    language = django_filters.CharFilter(name='word__language__language')
    target = django_filters.CharFilter(name='language__language')

    class Meta:
        model = Definition
        fields = ['word', 'language', 'username', 'definition', 'target', 'id']


class WordByURLWordFilter(filters.BaseFilterBackend):
    """
    Filter :model:`Word` by the url kwarg `word`.

    """

    def filter_queryset(self, request, queryset, view):
        if 'word' not in view.kwargs:
            return queryset
        else:
            word = view.kwargs['word']
            return queryset.filter(word=word)


class DefinitionByURLWordFilter(filters.BaseFilterBackend):
    """
    Filter :model:`Definition` by the url kwarg `word`.

    """

    def filter_queryset(self, request, queryset, view):
        if 'word' not in view.kwargs:
            return queryset
        else:
            word = view.kwargs['word']
            return queryset.filter(word__word=word)


class URLLanguageFilter(filters.BaseFilterBackend):
    """
    Filter :model:`Word` or :model:`Definition` by the url kwarg `language`.

    """

    def filter_queryset(self, request, queryset, view):
        language = view.kwargs['language']
        return queryset.filter(language__language=language)
