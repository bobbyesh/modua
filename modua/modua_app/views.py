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

from .utils import segmentize
from .mixins import LanguageFilterMixin

@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('language-list', request=request, format=format),
        })


class DefinitionListView(APIView, LanguageFilterMixin):
    """Defines a GET method to return json for an individual :model:`modua_app.Definitions`.


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
        queryset = Definitions.objects.filter(language=self.language)
        serializer = DefinitionsSerializer(queryset, many=True, context= {'request': request})
        return Response(serializer.data)




class DefinitionDetailView(APIView, LanguageFilterMixin):
    """Defines a GET method to return json for an individual :model:`modua_app.Definitions`.


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

        Overrides ListAPIView's get() method.

        :raises NotFound: Word not found in dictionary database.

        """
        queryset = Definitions.objects.filter(word=self.kwargs['word'], language=self.language)
        serializer = DefinitionsSerializer(queryset, context= {'request': request})
        return Response(serializer.data)


    def get_queryset(self):
        """Overrides ListAPIView's get_queryset() method.

        Returns a queryset of matches for 'word' URL keyword.

        """
        word = self.kwargs['word']
        if self.delimited:
            definitions = Definitions.objects.filter(
                    word=word,
                    language=self.language
            )
        else:
            segs = list(segmentize(self.kwargs['word']))
            definitions = Definitions.objects.filter(
                    word__in=segs,
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
