# filters.py

from rest_framework import filters
import django_filters
from .models import Word, Definition
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class WordFilter(filters.FilterSet):
    username = django_filters.CharFilter(name='owner__username')
    language = django_filters.CharFilter(name='language__language')
    article = django_filters.NumberFilter(name='articles__id')

    class Meta:
        model = Word
        fields = ['word', 'language', 'username', 'ease', 'article', 'id']


class DefinitionFilter(filters.FilterSet):
    word = django_filters.CharFilter(name='word__word')
    username = django_filters.CharFilter(name='owner__username')
    target = django_filters.CharFilter(name='language__language')

    class Meta:
        model = Definition
        fields = ['word', 'username', 'definition', 'id', 'target']



class URLKwargFilter(filters.BaseFilterBackend):
    """

    """

    def filter_queryset(self, request, queryset, view):
        query_kwargs = self.get_kwargs(request, queryset, view)
        return queryset.filter(**query_kwargs)

    def get_kwargs(self, request, queryset, view):
        query_kwargs = dict()
        if queryset.model == Word:
            if 'language' in view.kwargs:
                query_kwargs['language__language'] = view.kwargs['language']
            if 'word' in view.kwargs:
                query_kwargs['word'] = view.kwargs['word']

        elif queryset.model == Definition:
            if 'language' in view.kwargs:
                query_kwargs['word__language__language'] = view.kwargs['language']
            if 'word' in view.kwargs:
                query_kwargs['word__word'] = view.kwargs['word']

        return query_kwargs


class OwnerOnlyFilter(filters.BaseFilterBackend):
    """
    If request has a user, then give them all Public definitions and their own.
    Otherwise just give all public.

    """
    def filter_queryset(self, request, queryset, view):
        if type(request.user) is User:
            return queryset.filter(owner__in=[None, request.user])
        else:
            return queryset.filter(owner=None)


