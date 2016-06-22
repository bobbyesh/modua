from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse

from .models import Definitions
from .serializers import DefinitionsSerializer
from .utils import segmentize, is_delimited


class SearchView(APIView):

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
