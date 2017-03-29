# filters.py
import django_filters
from rest_framework import filters
from .models import PublicWord, PublicDefinition, UserWord, UserDefinition
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class PublicWordFilter(filters.FilterSet):
    class Meta:
        model = PublicWord
        fields = ['word', 'id']


class UserWordFilter(filters.FilterSet):
    username = django_filters.CharFilter(name='owner__username')
    article = django_filters.NumberFilter(name='articles__id')

    class Meta:
        model = UserWord
        fields = ['word', 'id', 'username', 'ease']


class PublicDefinitionFilter(filters.FilterSet):
    word = django_filters.CharFilter(name='word__word')

    class Meta:
        model = PublicDefinition
        fields = ['word', 'definition', 'id']


class UserDefinitionFilter(filters.FilterSet):
    word = django_filters.CharFilter(name='word__word')
    username = django_filters.CharFilter(name='owner__username')

    class Meta:
        model = UserDefinition
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
        if type(request.user) is User:
            return queryset.filter(owner=request.user)
        else:
            return queryset.filter(owner=None)


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
