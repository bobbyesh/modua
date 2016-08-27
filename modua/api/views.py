from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse

from .models import Definition, Language
from .serializers import (
        DefinitionSerializer,
        LanguageSerializer
        )

from .utils import segmentize, all_combinations
from .mixins import LanguageFilterMixin, MultipleFieldLookupMixin

import pdb


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('api:language-list', request=request, format=format),
        })


class DefinitionDetailView(RetrieveAPIView, MultipleFieldLookupMixin):
    queryset = Definition.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = DefinitionSerializer
    lookup_fields = ('word', 'language', 'id')


class DefinitionListView(ListAPIView):
    queryset = Definition.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = DefinitionSerializer

class LanguageListView(ListAPIView):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (AllowAny,)


class LanguageWordlistView(ListAPIView, LanguageFilterMixin):

    permission_classes = (AllowAny,)
    serializer_class = DefinitionSerializer

    def get_queryset(self):
        return Definition.objects.filter(language=self.language)