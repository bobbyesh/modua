from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.filters import DjangoFilterBackend

from rest_framework.exceptions import ValidationError
from wordfencer.parser import ChineseParser
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Definition, Word, UserWordData
from .filters import (
    PublicWordFilter,
    OwnerOnlyFilter,
    WordFilter,
    UserWordDataFilter,
    DefinitionFilter
)
from .serializers import PublicWordSerializer, UserWordDataSerializer, DefinitionSerializer
from .permissions import OnlyOwnerCanAccess, NoPutAllowed, OnlyEaseCanChange


parser = ChineseParser()


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'words': reverse('api:public-word-list', request=request, format=format),
        })


class DefinitionViewSet(viewsets.ModelViewSet):
    """Defines a list view for the `Definition` model that is only accessible by an authenticated user.

    This view should allow the creation and reading of definitions because user's can create and read definitions
    they have saved for themselves.

    """
    queryset = Definition.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    permission_classes = (OnlyOwnerCanAccess,)
    serializer_class = DefinitionSerializer
    filter_backends = (DjangoFilterBackend, OwnerOnlyFilter, WordFilter,)
    filter_class = DefinitionFilter

    def create(self, request, *args, **kwargs):
        """Example POST data:
        
            {
              "definition": "string123",
              "word": "A貨",
              "pinyin": "A huo4"
            }

        """
        pinyin = request.data['pinyin']

        word_obj = Word.objects.get_or_create(word=request.data['word'])
        user_word = UserWordData.objects.get(
            word=word_obj,
            owner=request.user,
        )
        definition = request.data['definition']
        definition, _ = Definition.objects.get_or_create(
            word=user_word,
            owner=request.user,
            definition=definition,
            pinyin=pinyin
        )
        data = {
            'word': {
                'id': user_word.id,
                'word': user_word.word,
                'ease': user_word.ease,
            },
            'definition': definition.definition,
            'id': definition.id,
            'pinyin': pinyin,
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Delete a definition.
        
        Example request:
        
            DELETE /api/user/definitions/2
        
        
        Will throw 404 if definition doesn't exist.
        """

        definition = get_object_or_404(Definition, id=kwargs['pk'], owner=request.user)
        definition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserWordViewSet(viewsets.ModelViewSet):
    """Defines a view for users to create, modify, or delete a single word in their account.

    The primary use of this view is adding a word to a user's account and changing the `ease` of a stored word as a learner comes to know the word more as
    time passes.
    """
    queryset = UserWordData.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (OnlyOwnerCanAccess, NoPutAllowed, OnlyEaseCanChange)
    serializer_class = UserWordDataSerializer
    filter_class = UserWordDataFilter
    filter_backends = (DjangoFilterBackend, OwnerOnlyFilter,)
    lookup_field = 'word'


class PublicWordViewSet(viewsets.ReadOnlyModelViewSet):
    """Defines a view for the `Word` model that is public accessible.

    This view should be read-only because the public should not be allowed to delete publically available
    words, this only the GET method is supported.

    """
    queryset = Word.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PublicWordSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PublicWordFilter
    lookup_field = 'word'


class PublicArticleView(APIView):
    """Requires 'title' and 'text' query parameters"""
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if 'title' not in request.data:
            raise ValidationError('missing the title parameter')

        if 'text' not in request.data:
            raise ValidationError('missing the text parameter')

        title = request.data['title']
        title = self.parse_into_json(title)
        text = request.data['text']
        paragraphs = []
        for splitted in text.split('\n'):
            paragraph = self.parse_into_json(splitted)
            paragraphs.append(paragraph)

        data = {
            'title': title,
            'paragraphs': paragraphs,
        }

        return Response(data)

    def parse_into_json(self, text):
        title_words = []
        parser_results = (p for p in parser.parse(text) if not p.isspace())
        for i, segment in enumerate(parser_results):
            words = Word.objects.filter(word=segment)
            if len(words) > 1:
                word = words[0].word
                pinyin = [w.pinyin for w in words]
            elif len(words) == 1:
                word = words[0].word
                pinyin = [words[0].pinyin]
            else:
                word = segment
                pinyin = []

            definitions = [d.definition for d in PublicDefinition.objects.filter(word__word=word)]
            title_words.append({
                'word': word,
                'index': i,
                'pinyin': pinyin,
                'definitions': definitions
            })

        return title_words