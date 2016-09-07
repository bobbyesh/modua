# filters.py

from rest_framework import filters
import django_filters
from .models import Word, Definition
from django.contrib.auth.models import User


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

    class Meta:
        model = Definition
        fields = ['word', 'username', 'definition', 'id']


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
        print("""here!!\n
              \nview: {}\n kwargs: {}\n query params: {}
        """.format(view, view.kwargs, request.query_params)
        )
        if queryset.model == Word:
            language = view.kwargs['language']
            return queryset.filter(language__language=language)

        elif queryset.model == Definition:
            language = view.kwargs['language']
            return queryset.filter(word__language__language=language)

        return queryset

class OwnerOnlyFilter(filters.BaseFilterBackend):
    """
    If request has a user, then give them all Public definitions and their own.
    Otherwise just give all public.

    """
    def filter_queryset(self, request, queryset, view):
        if type(request.user) is User:
            queryset.filter(owner__in=[None, request.user])
        else:
            return queryset.filter(owner=None)


