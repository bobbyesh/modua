from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from .models import Definitions, Languages
from .serializers import DefinitionsSerializer, LanguagesSerializer
from .utils import segmentize, is_delimited



class SearchView(APIView):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, language, word, format=None):
        if is_delimited(language):
            try:
                definition = Definitions.objects.get(word_character=word)
                serializer = DefinitionsSerializer(definition, many=False)
            except ObjectDoesNotExist:
                return Response(status=404)
        else:
            definitions = self.get_all_subsegment_definitions(word)
            if not definitions:
                return Response(status=404)
            elif len(definitions) == 1:
                only_definition = definitions[0]
                serializer = DefinitionsSerializer(only_definition, many=False)
            else:
                serializer = DefinitionsSerializer(definitions, many=True)

        return Response(serializer.data)

    def get_all_subsegment_definitions(self, word):
        definitions = list()
        for seg in segmentize(word):
            try:
                result = Definitions.objects.get(word_character=seg)
                definitions.append(result)
            except ObjectDoesNotExist:
                pass
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
