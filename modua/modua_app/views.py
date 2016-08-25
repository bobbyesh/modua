from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse

from .models import Definitions, Languages
from .serializers import (
        DefinitionsSerializer,
        LanguagesSerializer
        )

from .utils import segmentize, all_combinations
from .mixins import LanguageFilterMixin

import pdb


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('modua_app:language-list', request=request, format=format),
        })

class DefinitionListView(ListAPIView, LanguageFilterMixin):
    """Defines a GET method to return json for a list of :model:`modua_app.Definitions`.

    Read-only.


    Attributes
    ----------

    delimited : `boolean`
        True if language is delimited, otherwise False. Inherited from `LanguageFilterMixin`.

    language: :model:`modua_app.models.Languages`
        Model instance matching URL keyword `language`. Inherited from `LanguageFilterMixin`

    Other attributes, args, and kwargs are the same as ListAPIView.

    """

    queryset = Definitions.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = DefinitionsSerializer


    def get(self, request, format=None, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response(status=404)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DefinitionsSerializer(page, many=True, context= {'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = DefinitionsSerializer(queryset, many=True, context= {'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        """If the URL doesn't contain a keyword `word`, then return all words in the language.
        Otherwise, return all words in the language matching the keyword `word`.

        """
        if 'word' not in self.kwargs:
            return self.get_all_words()

        return self.get_word_subset()

    def get_all_words(self):
        """Returns a queryset of all the words in URL keyword 'language'"""
        queryset = Definitions.objects.filter(language=self.language)
        return queryset

    def get_word_subset(self):
        """Returns a queryset of matches for 'word' and 'language' URL keywords."""
        word = self.kwargs['word']
        if self.delimited:
            queryset = Definitions.objects.filter(
                word=word,
                language=self.language
            )
        else:
            queryset = Definitions.objects.filter(
                word__in=all_combinations(word),
                language=self.language
            )
        return queryset




class DefinitionGenericView(APIView, LanguageFilterMixin):
    """Defines a GET method to return json for an individual or a list of :model:`modua_app.Definitions`.


    Attributes
    ----------

    delimited : `boolean`
        True if language is delimited, otherwise False. Inherited from `LanguageFilterMixin`.

    language: :model:`modua_app.models.Languages`
        Model instance matching URL keyword `language`. Inherited from `LanguageFilterMixin`

    Other attributes, args, and kwargs are the same as APIView.

    """

    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, format=None, *args, **kwargs):
        """Get a word definition.

        Overrides APIView's get() method.

        :raises NotFound: Word not found in dictionary database.

        """
        queryset = self.get_queryset()
        if not queryset:
            return Response(status=404)
        serializer = DefinitionsSerializer(queryset, many=True, context= {'request': request})
        return Response(serializer.data)


    def get_queryset(self):
        """Returns a queryset of matches for 'word' URL keyword.

        """
        word = self.kwargs['word']
        if self.delimited:
            definitions = Definitions.objects.filter(
                word=word,
                language=self.language
            )
        else:
            definitions = Definitions.objects.filter(
                word__in=all_combinations(word),
                language=self.language
            )
        return definitions


class LanguageListView(ListAPIView):

    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer
    permission_classes = (AllowAny,)


class LanguageWordlistView(ListAPIView, LanguageFilterMixin):

    permission_classes = (AllowAny,)
    serializer_class = DefinitionsSerializer

    def get_queryset(self):
        return Definitions.objects.filter(language=self.language)
