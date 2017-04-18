# filters.py
import django_filters
from rest_framework import filters
from .models import Word, UserWordData, Definition
from django.contrib.auth.models import User


class PublicWordFilter(filters.FilterSet):
    class Meta:
        model = Word
        fields = ['word', 'id']


class UserWordDataFilter(filters.FilterSet):
    username = django_filters.CharFilter(name='owner__username')
    article = django_filters.NumberFilter(name='articles__id')

    class Meta:
        model = UserWordData
        fields = ['word', 'id', 'username', 'ease']


class DefinitionFilter(filters.FilterSet):
    word = django_filters.CharFilter(name='word__word')
    username = django_filters.CharFilter(name='owner__username')

    class Meta:
        model = Definition
        fields = ['word', 'definition', 'id', 'username']


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
        return queryset.filter(owner=request.user)


class WordFilter(filters.BaseFilterBackend):
    """
    If request has a user, then give them all Public definitions and their own.
    Otherwise just give all public.

    """
    def filter_queryset(self, request, queryset, view):
        if 'word' in request.query_params:
            return queryset.filter(word__word=request.query_params['word'])
        else:
            return queryset
