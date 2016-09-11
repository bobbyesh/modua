from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
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
from rest_framework.exceptions import NotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from wordfencer.parser import ChineseParser
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError

from core.services import fetch_article
from core.decorators import find_language_or_404, required_request_data
from core.exceptions import Raise403
from .models import PublicDefinition, UserDefinition, Language, Article, PublicWord, UserWord
from .filters import PublicWordFilter, PublicDefinitionFilter, OwnerOnlyFilter, URLKwargFilter, OwnerWordOnlyFilter, UserWordFilter, LanguageFilter, UserDefinitionFilter
from .serializers import PublicDefinitionSerializer, LanguageSerializer, PublicWordSerializer, TokenSerializer, UserWordSerializer, UserDefinitionSerializer
from .mixins import LanguageFilterMixin
from core.utils import Token, get_object_or_403
from .permissions import OnlyOwnerCanAccess, OnlyOwnerCanDelete, NoPutAllowed, OnlyEaseCanChange


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('language-list', request=request, format=format),
        })


class PublicDefinitionListView(ListAPIView):
    """Defines a list view for the `PublicDefinition` model that is publically accessible.

    This view should be read-only, as public information should be protected from deletion.
    This means that only the GET method need be supported.


    .. todo: Change OwnerOnlyFilter to PublicFilter for clarity

    """
    queryset = PublicDefinition.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = PublicDefinitionSerializer
    filter_backends = (URLKwargFilter, DjangoFilterBackend,)
    filter_class = PublicDefinitionFilter


class UserDefinitionListView(ListAPIView):
    """Defines a list view for the `Definition` model that is only accessible by an authenticated user.

    This view should allow the creation and reading of definitions because user's can create and read definitions
    they have saved for themselves.

    :Supported Methods:

        GET, POST

    """
    queryset = UserDefinition.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (OnlyOwnerCanAccess,)
    serializer_class = UserDefinitionSerializer
    filter_backends = (URLKwargFilter, DjangoFilterBackend, OwnerOnlyFilter,)
    filter_class = UserDefinitionFilter


class UserDefinitionCreateDestroyView(CreateAPIView, DestroyAPIView):
    queryset = UserDefinition.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (OnlyOwnerCanAccess,)
    serializer_class = UserDefinitionSerializer
    filter_backends = (URLKwargFilter, DjangoFilterBackend, OwnerOnlyFilter,)
    filter_class = UserDefinitionFilter

    @find_language_or_404
    @required_request_data(['target', 'definition'])
    def create(self, request, *args, **kwargs):
        definition = self.get_definition()
        serializer = UserDefinitionSerializer(definition)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_definition(self):
        try:
            definition = UserDefinition.objects.create(
                word=self.get_word(),
                definition=self.request.data['definition'],
                language=self.get_target(),
                owner=self.request.user
            )
        except IntegrityError:
            raise Raise403(detail={'message': 'User already has this definition saved for this word'})

        return definition

    def get_word(self):
        try:
            word = UserWord.objects.get(**self.get_word_fields())
        except ObjectDoesNotExist:
            message = (
                'The definition could not be created because word {} in language {} does'
                'not exist for user {}'
            ).format(self.kwargs['word'], self.get_word_fields()['language'], self.request.user)

            raise NotFound(detail={'message': message})

        return word

    def get_target(self):
        try:
            target = Language.objects.get(language=self.request.data['target'])
        except ObjectDoesNotExist:
            raise NotFound(detail={'message': 'Target language {} is not currently supported or does not exist.'.format(self.request.data['target'])})

        return target

    def get_word_fields(self):
        return {
            'language': Language.objects.get(language=self.kwargs['language']),
            'word': self.kwargs['word'],
            'owner': self.request.user,
        }


class UserWordDetailView(CreateModelMixin, RetrieveUpdateAPIView):
    """Defines a view for users to create, modify, or delete a single word in their account.

    The primary use of this view is adding a word to a user's account and changing the `ease` of a stored word as a learner comes to know the word more as 
    time passes.

    :Supported Methods:
        GET, POST, PATCH

    """
    http_method_names = ['get', 'post', 'patch']
    queryset = UserWord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (OnlyOwnerCanAccess, NoPutAllowed, OnlyEaseCanChange)
    serializer_class = UserWordSerializer
    filter_class = UserWordFilter
    filter_backends = (DjangoFilterBackend, OwnerOnlyFilter, URLKwargFilter)
    lookup_field = 'word'
    lookup_url_kwarg = 'word'

    @find_language_or_404
    def post(self, request, *args, **kwargs):
        message = ('User already has this word saved, either delete and then post the'
                   'word, or just update it.')
        word = get_object_or_403(UserWord, message=message, **self.build_fields())
        serializer = UserWordSerializer(word)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def build_fields(self):
        ease = self.request.data['ease'] if 'ease' in self.request.data else ''
        transliteration = self.request.data['translation'] if 'translation' in self.request.data else ''
        return {
            'language': Language.objects.get(language=self.kwargs['language']),
            'word': self.kwargs['word'],
            'owner': self.request.user,
            'ease': ease,
            'transliteration': transliteration
        }


class PublicWordListView(ListAPIView):
    """Defines a view for the `Word` model that is public accessible.

    This view should be read-only because the public should not be allowed to delete publically available
    words, this only the GET method is supported.

    """
    queryset = PublicWord.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PublicWordSerializer
    filter_backends = (URLKwargFilter, DjangoFilterBackend,)
    filter_class = PublicWordFilter


class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (AllowAny,)



class ParseView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if self.request.data['language'] == 'zh':
            string = request.data['string']
            parser = ChineseParser()
            segments = parser.parse(string)
            return Response(data=segments)
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
