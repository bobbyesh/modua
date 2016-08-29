from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from core.utils import all_combinations
from .mixins import LanguageFilterMixin
from .models import Definition, Language
from .serializers import (
        DefinitionSerializer,
        LanguageSerializer
        )


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('api:language-list', request=request, format=format),
        })

class DefinitionListView(ListAPIView, LanguageFilterMixin):
    """Defines a GET method to return json for a list of :model:`api.Definition`.

    Read-only.


    Attributes
    ----------

    delimited : `boolean`
        True if language is delimited, otherwise False. Inherited from `LanguageFilterMixin`.

    language: :model:`api.models.Language`
        Model instance matching URL keyword `language`. Inherited from `LanguageFilterMixin`

    Other attributes, args, and kwargs are the same as ListAPIView.

    """

    queryset = Definition.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = DefinitionSerializer


    def get(self, request, format=None, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response(status=404)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DefinitionSerializer(page, many=True, context= {'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = DefinitionSerializer(queryset, many=True, context= {'request': request})
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
        queryset = Definition.objects.filter(language=self.language)
        return queryset

    def get_word_subset(self):
        """Returns a queryset of matches for 'word' and 'language' URL keywords."""
        word = self.kwargs['word']
        if self.delimited:
            queryset = Definition.objects.filter(
                word=word,
                language=self.language
            )
        else:
            queryset = Definition.objects.filter(
                word__in=all_combinations(word),
                language=self.language
            )
        return queryset




class DefinitionGenericView(APIView, LanguageFilterMixin):
    """Defines a GET method to return json for an individual or a list of :model:`api.Definition`.


    Attributes
    ----------

    delimited : `boolean`
        True if language is delimited, otherwise False. Inherited from `LanguageFilterMixin`.

    language: :model:`api.models.Language`
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
        serializer = DefinitionSerializer(queryset, many=True, context= {'request': request})
        return Response(serializer.data)


    def get_queryset(self):
        """Returns a queryset of matches for 'word' URL keyword.

        """
        word = self.kwargs['word']
        if self.delimited:
            definitions = Definition.objects.filter(
                word=word,
                language=self.language
            )
        else:
            definitions = Definition.objects.filter(
                word__in=all_combinations(word),
                language=self.language
            )
        return definitions


class LanguageListView(ListAPIView):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (AllowAny,)


class LanguageWordlistView(ListAPIView, LanguageFilterMixin):

    permission_classes = (AllowAny,)
    serializer_class = DefinitionSerializer

    def get_queryset(self):
        return Definition.objects.filter(language=self.language)
