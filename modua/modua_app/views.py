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



class SearchView(ListAPIView):

    queryset = Definitions.objects.all()
    serializer_class = DefinitionsSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    # TODO implement get() with default list(), but return 404 if list() returns response
    # with no data
    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        if not response.data:
            return Response(status=404)
        return self.list(request, *args, **kwargs)


    '''
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response(status=404)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    '''

    def get_queryset(self):
        lang = self.kwargs['language']
        word = self.kwargs['word']
        if is_delimited(lang):
            definitions = Definitions.objects.filter(
                    word_character=word,
                    fk_definitionlang=
                        Languages.objects.filter(
                            language=lang
                        )
            )
        else:
            definitions = None
            segs = list(segmentize(self.kwargs['word']))
            definitions = Definitions.objects.filter(
                    word_character__in=segs,
                    fk_definitionlang=
                        Languages.objects.filter(
                            language=lang
                    )
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
