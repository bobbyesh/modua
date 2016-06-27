import pdb
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from .models import Definitions, Languages
from .serializers import DefinitionsSerializer, LanguagesSerializer
from .utils import segmentize, is_delimited


class LanguageFilterMixin(object):
    '''
    Use for views that require identifying a single language from the
    'language' url keyword.

    The set_language method automatically sets self.language to the
    associated model instance, and sets self.delimited to True if the
    language is delimited and False otherwise.
    '''

    def set_language(self):
        self.language = Languages.objects.filter(
                language=self.kwargs['language']
        )
        self.delimited = is_delimited(self.language)


class SearchView(ListAPIView, LanguageFilterMixin):

    queryset = Definitions.objects.all()
    serializer_class = DefinitionsSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        if not response.data:
            return Response(status=404)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        self.set_language()
        word = self.kwargs['word']
        if self.delimited:
            definitions = Definitions.objects.filter(
                    word_character=word,
                    fk_definitionlang=self.language
            )
        else:
            segs = list(segmentize(self.kwargs['word']))
            definitions = Definitions.objects.filter(
                    word_character__in=segs,
                    fk_definitionlang=self.language
            )

        return definitions


class LanguageListView(ListAPIView):

    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer
    permission_classes = (AllowAny,)
    lookup_fields = ('language',)


class LanguageWordlistView(ListAPIView):

    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = DefinitionsSerializer

    def get_queryset(self):
        lang = self.kwargs['language']
        language_query = Languages.objects.filter(language=lang)
        return Definitions.objects.filter(fk_definitionlang=language_query)
