from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from rest_framework.generics import ListAPIView, GenericAPIView
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

import pdb

@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('language_list', request=request, format=format),
        })

class SearchView(ListAPIView, LanguageFilterMixin):
    """Handles requests searching for the definition of a word.

    Inherits `language` property from LanguageFilterMixin.  This
    property is the Languages model associated with the url keyword
    matched to 'language', and is used when querying for a word in
    a particular language.

    """

    queryset = Definitions.objects.all()
    serializer_class = DefinitionsSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        """
        GET request for word definition.  Overrides ListAPIView's get() method.
        
        URL keywords: word, language.

        self.language is the matching language, if any. 
        (inherited from LanguageFilterMixin)
        
        :ivar delimited: boolean; True if language is delimited, otherwise False.
        :ivar language: Languages model instance matching URL keyword 'language'.

        :raises NotFound: Word not found in dictionary database.

        """

        response = self.list(request, *args, **kwargs)
        if not response.data:
            raise NotFound
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """Overrides ListAPIView's get_queryset() method.

        Returns a queryset of matches for 'word' URL keyword.
        
        """
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
