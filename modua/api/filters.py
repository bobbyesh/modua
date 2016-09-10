# filters.py

from rest_framework import filters
import django_filters
from .models import PublicWord, PublicDefinition, UserWord, UserDefinition
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class PublicWordFilter(filters.FilterSet):
    language = django_filters.CharFilter(name='language__language')

    class Meta:
        model = PublicWord
        fields = ['word', 'language', 'id']


class UserWordFilter(filters.FilterSet):
    username = django_filters.CharFilter(name='owner__username')
    language = django_filters.CharFilter(name='language__language')
    article = django_filters.NumberFilter(name='articles__id')

    class Meta:
        model = UserWord
        fields = ['word', 'language', 'id', 'username', 'ease']


class PublicDefinitionFilter(filters.FilterSet):
    word = django_filters.CharFilter(name='word__word')
    target = django_filters.CharFilter(name='language__language')

    class Meta:
        model = PublicDefinition
        fields = ['word', 'definition', 'id', 'target']


class UserDefinitionFilter(filters.FilterSet):
    word = django_filters.CharFilter(name='word__word')
    target = django_filters.CharFilter(name='language__language')
    username = django_filters.CharFilter(name='owner__username')

    class Meta:
        model = UserDefinition
        fields = ['word', 'definition', 'id', 'target', 'username']


class LanguageFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        query_kwargs = self.get_kwargs(request, queryset, view)
        return queryset.filter(**query_kwargs)

    def get_kwargs(self, request, queryset, view):
        query_kwargs = dict()
        if (queryset.model == PublicWord or
            queryset.model == UserWord):
            if 'language' in view.kwargs:
                query_kwargs['language__language'] = view.kwargs['language']

        elif (queryset.model == PublicDefinition or
              queryset.model == UserDefinition):
            if 'language' in view.kwargs:
                query_kwargs['word__language__language'] = view.kwargs['language']


class URLKwargFilter(filters.BaseFilterBackend):
    """

    """

    def filter_queryset(self, request, queryset, view):
        query_kwargs = self.get_kwargs(request, queryset, view)
        return queryset.filter(**query_kwargs)

    def get_kwargs(self, request, queryset, view):
        query_kwargs = dict()
        if (queryset.model == PublicWord or
            queryset.model == UserWord):
            if 'language' in view.kwargs:
                query_kwargs['language__language'] = view.kwargs['language']
            if 'word' in view.kwargs:
                query_kwargs['word'] = view.kwargs['word']

        elif (queryset.model == UserDefinition or
              queryset.model == PublicDefinition):
            if 'language' in view.kwargs:
                query_kwargs['word__language__language'] = view.kwargs['language']
            if 'word' in view.kwargs:
                query_kwargs['word__word'] = view.kwargs['word']

        return query_kwargs


class OwnerWordOnlyFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if type(request.user) is User:
            return queryset.filter(owner=request.user)
        else:
            return queryset.none()


class OwnerOnlyFilter(filters.BaseFilterBackend):
    """
    If request has a user, then give them all Public definitions and their own.
    Otherwise just give all public.

    """
    def filter_queryset(self, request, queryset, view):
        if type(request.user) is User:
            return queryset.filter(owner=request.user)
        else:
            return queryset.filter(owner=None)


