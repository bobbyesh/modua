from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from .models import Definitions, Languages
from .serializers import (
        DefinitionsSerializer, 
        DefinitionsListSerializer, 
        LanguagesSerializer
        )

from .utils import segmentize
from .mixins import LanguageFilterMixin

import pdb

class APIRoot(GenericAPIView):
    pass

class SearchView(ListAPIView, LanguageFilterMixin):

    queryset = Definitions.objects.all()
    serializer_class = DefinitionsSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        if not response.data:
            raise NotFound
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
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


class LanguageWordlistView(ListAPIView, LanguageFilterMixin):

    permission_classes = (AllowAny,)
    serializer_class = DefinitionsSerializer

    def get_queryset(self):
        return Definitions.objects.filter(fk_definitionlang=self.language)
