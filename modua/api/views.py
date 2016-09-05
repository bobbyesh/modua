from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from wordfencer.parser import ChineseParser

from core.services import fetch_article
from .models import Definition, Language, Article, Word
from .serializers import DefinitionSerializer, LanguageSerializer, WordSerializer
from .mixins import LanguageFilterMixin


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'languages': reverse('language-list', request=request, format=format),
        })




class UpdateWordView(UpdateAPIView, LanguageFilterMixin):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)
    serializer_class = WordSerializer

    def patch(self, request, *args, **kwargs):
        username = request.query_params['username']
        password = request.query_params['password']
        assert username == self.request.user.username
        assert password == self.request.user.password

        words = Word.objects.filter(word=self.request.data['word'], language=self.language, users__username=self.request.user.username)
        if len(words) > 1:
            raise Exception("There should not be more than one word per user")
        if len(words) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        word = words[0]
        if 'ease' in request.query_params:
            word.ease = request.query_params['ease']
            word.save()

        serializer = WordSerializer(word)
        return Response(serializer.data)








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


class WordDetailView(RetrieveAPIView, UpdateAPIView, LanguageFilterMixin):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (AllowAny,)
    serializer_class = WordSerializer

    lookup_field = 'word'
    lookup_url_kwarg = 'word'

    def get_queryset(self):
        return Word.objects.filter(language=self.language)


    def patch(self, request, *args, **kwargs):
        username = request.query_params['username']
        password = request.query_params['password']
        assert username == self.request.user.username
        assert password == self.request.user.password

        words = Word.objects.filter(word=self.request.data['word'], language=self.language, users__username=self.request.user.username)
        if len(words) > 1:
            raise Exception("There should not be more than one word per user")
        if len(words) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        word = words[0]
        if 'ease' in request.query_params:
            word.ease = request.query_params['ease']
            word.save()

        serializer = WordSerializer(word)
        return Response(serializer.data)



class DefinitionDetailView(RetrieveAPIView, UpdateAPIView, LanguageFilterMixin):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (AllowAny,)
    serializer_class = WordSerializer

    def get(self, request, *args, **kwargs):
        word = kwargs['word']
        id = int(kwargs['id'])
        try:
            result = Word.objects.get(id=id, word=word, language=self.language)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(result, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        username = request.query_params['username']
        password = request.query_params['password']
        assert username == self.request.user.username
        assert password == self.request.user.password

        words = Word.objects.filter(word=self.request.data['word'], language=self.language, users__username=self.request.user.username)
        if len(words) > 1:
            raise Exception("There should not be more than one word per user")
        if len(words) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        word = words[0]
        if 'ease' in request.query_params:
            word.ease = request.query_params['ease']
            word.save()

        serializer = WordSerializer(word)
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
        try:
            word = self.get_word()
        except:
            return []
        return Definition.objects.filter(word=word, language=self.target)

    def all_translations_for_word(self):
        try:
            word = self.get_word()
        except:
            return []
        return Definition.objects.filter(word=word)

    def get_word(self):
        return Word.objects.get(word=self.kwargs['word'], language=self.language)

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

