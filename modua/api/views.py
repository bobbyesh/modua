from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.filters import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.mixins import LoginRequiredMixin
from wordfencer.parser import ChineseParser
from django.shortcuts import get_object_or_404

from core.services import fetch_article
from .models import Definition, Language, Article, Word
from .filters import WordFilter, DefinitionFilter, WordByURLWordFilter, DefinitionByURLWordFilter, URLLanguageFilter
from .serializers import DefinitionSerializer, LanguageSerializer, WordSerializer, TokenSerializer
from .mixins import LanguageFilterMixin
from core.utils import Token
from .permissions import OnlyOwnerCanAccess, OnlyOwnerCanDelete


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('language-list', request=request, format=format),
        })


class DefinitionDetailView(RetrieveDestroyAPIView):
    queryset = Definition.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (AllowAny, OnlyOwnerCanAccess, OnlyOwnerCanDelete,)
    serializer_class = DefinitionSerializer
    filter_class = DefinitionFilter
    filter_backends = (DjangoFilterBackend,)
    lookup_field = 'definition'


class WordDetailView(RetrieveUpdateAPIView, LanguageFilterMixin):
    queryset = Word.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (AllowAny, OnlyOwnerCanAccess)
    serializer_class = WordSerializer
    filter_class = WordFilter
    filter_backends = (DjangoFilterBackend,)
    lookup_field = 'word'
    lookup_url_kwarg = 'word'


class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (AllowAny,)


class DefinitionListView(ListAPIView):
    queryset = Definition.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (AllowAny, OnlyOwnerCanAccess)
    serializer_class = DefinitionSerializer
    filter_backends = (DjangoFilterBackend, URLLanguageFilter, DefinitionByURLWordFilter,)
    filter_class = DefinitionFilter


class ParseView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if request.data['language'] == 'zh':
            string = request.data['string']
            parser = ChineseParser()
            segments = parser.parse(string)
            token_list = [Token(string=seg, position=idx) for idx, seg in enumerate(segments)]
            serializer = TokenSerializer(token_list, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class URLImportView(APIView, LanguageFilterMixin, LoginRequiredMixin):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not self.language:
            return Response(
                {
                    'message': 'Language "{}" not found'.format(request.data['language']),
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if request.data['language'] == 'zh':
            language = request.data['language']
            url = request.data['url']
            article = Article.objects.filter(url=url)
            if not article:
                title, text = fetch_article(url, language)
                Article.objects.create(title=title, text=text, url=url, language=self.language, owner=user)

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


