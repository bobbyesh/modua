from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from wordfencer.parser import ChineseParser

from .models import Definition, Language
from .serializers import DefinitionSerializer, LanguageSerializer
from .mixins import LanguageFilterMixin


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('language-list', request=request, format=format),
        })


class SentenceView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, language):
        if language == 'zh':
            parser = ChineseParser()
            tokens = parser.parse(request.data['sentence'])
            language_query = Language.objects.get(language='zh')
            queryset = Definition.objects.filter(word__in=tokens, language=language_query)
            serializer = DefinitionSerializer(queryset)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DefinitionDetailView(RetrieveAPIView, LanguageFilterMixin):
    queryset = Definition.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = DefinitionSerializer

    def get(self, request, *args, **kwargs):
        word = kwargs['word']
        id = kwargs['id']
        result = get_object_or_404(Definition, id=id, word=word, language=self.language)
        serializer = self.get_serializer(result, many=False)
        return Response(serializer.data)




class DefinitionListView(ListAPIView, LanguageFilterMixin):
    queryset = Definition.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = DefinitionSerializer

    def list(self, request, *args, **kwargs):
        if self.requesting_one_word() and self.requesting_target_language_translation():
            queryset = self.single_word_to_target_language()
        elif self.requesting_one_word() and not self.requesting_target_language_translation():
            queryset = self.all_translations_for_word()
        else:
            queryset = self.all_words_in_language()

        serializer = DefinitionSerializer(queryset, many=True)

        if len(queryset) == 0:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    def single_word_to_target_language(self):
        return Definition.objects.filter(word=self.kwargs['word'], language=self.language, target=self.target)

    def all_translations_for_word(self):
        return Definition.objects.filter(word=self.kwargs['word'], language=self.language)

    def all_words_in_language(self):
        return Definition.objects.filter(language=self.language)

    def requesting_one_word(self):
        return 'word' in self.kwargs

    def requesting_target_language_translation(self):
        return 'target' in self.request.query_params

    def requesting_all_translations(self):
        return 'word' in self.kwargs and 'target' not in self.request.query_params

    def requesting_all_words_in_language(self):
        return 'word' not in self.kwargs



class LanguageListView(ListAPIView):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (AllowAny,)

