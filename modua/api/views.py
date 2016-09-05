from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.filters import DjangoFilterBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from wordfencer.parser import ChineseParser
from django.shortcuts import get_object_or_404


from core.services import fetch_article
from .models import Definition, Language, Article, Word
from .filters import WordFilter, DefinitionFilter
from .serializers import DefinitionSerializer, LanguageSerializer, WordSerializer
from .mixins import LanguageFilterMixin


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('language-list', request=request, format=format),
        })


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


class AnnotationView(APIView, LanguageFilterMixin):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if request.data['language'] == 'zh':
            parser = ChineseParser()
            tokens = parser.parse(request.data['string'])
            serialized = []
            for t in tokens:
                qset = Definition.objects.filter(word=t, language=self.language, target=self.target)
                serializer = DefinitionSerializer(qset, many=True)
                serialized.append(serializer.data)

            if len(serialized) == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(serialized)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class WordDetailView(RetrieveUpdateAPIView, LanguageFilterMixin):
    queryset = Word.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (AllowAny,)

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
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (AllowAny,)

    serializer_class = DefinitionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = DefinitionFilter
