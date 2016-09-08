from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
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
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from wordfencer.parser import ChineseParser
from django.shortcuts import get_object_or_404

from core.services import fetch_article
from .models import Definition, Language, Article, Word
from .filters import WordFilter, DefinitionFilter, OwnerOnlyFilter, URLKwargFilter, OwnerWordOnlyFilter, LanguageFilter
from .serializers import DefinitionSerializer, LanguageSerializer, WordSerializer, TokenSerializer
from .mixins import LanguageFilterMixin
from core.utils import Token
from .permissions import OnlyOwnerCanAccess, OnlyOwnerCanDelete, NoPutAllowed, OnlyEaseCanChange


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('language-list', request=request, format=format),
        })


class DefinitionListView(ListAPIView):
    """Defines a list view for the `Definition` model that is publically accessible.

    This view should be read-only, as public information should be protected from deletion.
    This means that only the GET method need be supported.


    .. todo: Change OwnerOnlyFilter to PublicFilter for clarity

    """
    queryset = Definition.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (OnlyOwnerCanAccess,)
    serializer_class = DefinitionSerializer
    filter_backends = (URLKwargFilter, DjangoFilterBackend, OwnerOnlyFilter,)
    filter_class = DefinitionFilter


class UserDefinitionListView(ListAPIView):
    """Defines a list view for the `Definition` model that is only accessible by an authenticated user.

    This view should allow the creation and reading of definitions because user's can create and read definitions
    they have saved for themselves.

    :Supported Methods:

        GET, POST

    """
    pass


class UserDefinitionDetailView(APIView):
    pass


class UserWordDetailView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    """Defines a view for users to create, modify, or delete a single word in their account.  Initially, as out of the box parsing won't
    support user-definied strings, this view will be used to simply add words to the user's own account.  Later, 
    they should be able to add words of their own choosing and length.

    The primary use of this view is adding a word to a user's account and changing the `ease` of a stored word as a learner comes to know the word more as 
    time passes.

    :Supported Methods:
        GET, POST, PATCH, DELETE

    """
    queryset = Word.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (OnlyOwnerCanAccess, NoPutAllowed, OnlyEaseCanChange)
    serializer_class = WordSerializer
    filter_class = WordFilter
    filter_backends = (DjangoFilterBackend, OwnerOnlyFilter, URLKwargFilter)
    lookup_field = 'word'
    lookup_url_kwarg = 'word'

    def create(self, request, *args, **kwargs):
        language = self.kwargs['language']
        word = self.kwargs['word']
        language = Language.objects.get(language=language)
        word_instance = Word.objects.create(language=language, word=word, owner=request.user, **request.data)
        serializer = WordSerializer(word_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PublicWordListView(ListAPIView):
    """Defines a view for the `Word` model that is public accessible.

    This view should be read-only because the public should not be allowed to delete publically available
    words, this only the GET method is supported.

    """
    pass


class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (AllowAny,)



class ParseView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if self.kwargs['language'] == 'zh':
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


############################################################################

"""The following classes all need refactoring."""

############################################################################


class DefinitionDetailView(RetrieveDestroyAPIView):
    queryset = Definition.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (AllowAny, OnlyOwnerCanAccess, OnlyOwnerCanDelete,)
    serializer_class = DefinitionSerializer
    filter_class = DefinitionFilter
    filter_backends = (DjangoFilterBackend,)
    lookup_field = 'definition'


class WordDetailView(RetrieveUpdateAPIView, LanguageFilterMixin):
    """

    ..TODO:  Only allow authorized, and don't allow multiple identical words per user.

    """
    queryset = Word.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny, OnlyOwnerCanAccess)
    serializer_class = WordSerializer
    filter_class = WordFilter
    filter_backends = (DjangoFilterBackend, OwnerOnlyFilter, URLKwargFilter)
    lookup_field = 'word'
    lookup_url_kwarg = 'word'


class WordCreateView(CreateAPIView):
    """

    .. TODO:  Hand roll this view.

    """
    queryset = Word.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny, OnlyOwnerCanAccess)
    serializer_class = WordSerializer
    filter_class = WordFilter
    filter_backends = (DjangoFilterBackend, LanguageFilter,)
    lookup_field = 'word'
    lookup_url_kwarg = 'word'

    def post(self, request, *args, **kwargs):
        if request.auth:
            language = Language.objects.get(language=kwargs['language'])
            word = Word.objects.create(word=kwargs['word'], language=language, user=request.user)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(word)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
