from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from mock import patch

from .serializers import DefinitionSerializer
from .models import Definition, User, Language
from .views import LanguageListView, DefinitionListView, DefinitionDetailView, AnnotationView


class LanguageListTestCase(APITestCase):

    def setUp(self):
        Language.objects.create(language='en')
        Language.objects.create(language='zh')

    def test_list_results(self):
        view = LanguageListView.as_view()
        factory = APIRequestFactory()
        request = factory.get('/api/0.1/languages/')
        response = view(request)
        self.assertContains(response, 'en')
        self.assertContains(response, 'zh')


class DefinitionListTestCase(APITestCase):

    def setUp(self):
        language = Language.objects.create(language='en')
        Definition.objects.create(
            language=language,
            target=language,
            word='cool',
            translation='not hot',
        )

        Definition.objects.create(
            language=language,
            target=language,
            word='building',
            translation='a thing in cities',
        )

        chinese = Language.objects.create(language='zh')

        Definition.objects.create(
            language=chinese,
            target=chinese,
            word='chineseword',
            translation='some translation',
        )
        view = DefinitionListView.as_view()
        factory = APIRequestFactory()
        request = factory.get('/api/0.1/languages/en/cool/')
        self.response = view(request, language='en', word='cool')

    def test_does_contain_word(self):
        self.assertContains(self.response, 'cool')

    def test_does_not_contain_different_word_same_language(self):
        self.assertNotContains(self.response, 'building')

    def test_does_not_contain_different_language(self):
        self.assertNotContains(self.response, 'chineseword')


class DefinitionDetailTestCase(APITestCase):

    def setUp(self):
        language = Language.objects.create(language='en')
        Definition.objects.create(
            language=language,
            target=language,
            word='cool',
            translation='not hot',
        )
        self.view = DefinitionDetailView.as_view()
        self.factory = APIRequestFactory()

    def test_does_contain_word(self):
        request = self.factory.get('/api/0.1/languages/en/cool/1/')
        self.response = self.view(request, language='en', word='cool', id='1')
        self.assertContains(self.response, 'cool')

    def test_wrong_language_raises_404(self):
        request = self.factory.get('/api/0.1/languages/zh/cool/2/')
        response = self.view(request, language='zh', word='cool', id='2')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_word_raises_404(self):
        request = self.factory.get('/api/0.1/languages/en/basketball/3/')
        response = self.view(request, language='en', word='basketball', id='3')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_id_raises_404(self):
        request = self.factory.get('/api/0.1/languages/en/cool/9999/')
        response = self.view(request, language='en', word='cool', id='9999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AnnotateTestCase(APITestCase):
    def setUp(self):
        english = Language.objects.create(language='en')
        chinese = Language.objects.create(language='zh')
        Definition.objects.create(
            language=chinese,
            target=english,
            word='我',
            translation='I',
        )
        Definition.objects.create(
            language=chinese,
            target=english,
            word='是',
            translation='am',
        )
        Definition.objects.create(
            language=chinese,
            target=english,
            word='美国',
            translation='America',
        )
        Definition.objects.create(
            language=chinese,
            target=english,
            word='人',
            translation='person',
        )
        self.view = AnnotationView.as_view()
        self.factory = APIRequestFactory()

    @patch('wordfencer.parser.ChineseParser.parse')
    def test_correct_query_status_200(self, parse):
        parse.return_value = ['我','是','美国','人']
        url = '/api/0.1/annotate/?string=我是美国人&language=zh&target=en'
        request = self.factory.post(url, {'string': '我是美国人', 'language': 'zh', 'target': 'en'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('wordfencer.parser.ChineseParser.parse')
    def test_correct_query_result(self, parse):
        tokens = ['我','是','美国','人']
        parse.return_value = tokens
        url = '/api/0.1/annotate/?string=我是美国人&language=zh&target=en'
        request = self.factory.post(url, {'string': '我是美国人', 'language': 'zh', 'target': 'en'})
        response = self.view(request)

        expected = self.expected_result(tokens)
        self.assertEqual(response.data, expected)

    def expected_result(self, tokens):
        language = Language.objects.get(language='zh')
        target = Language.objects.get(language='en')
        queryset = Definition.objects.filter(word__in=tokens, language=language, target=target)
        serializer = DefinitionSerializer(queryset, many=True)
        return serializer.data


    def test_empty_query_returns_404(self):
        url = '/api/0.1/annotate/?string&language=zh&target=en'
        request = self.factory.post(url, {'string': '', 'language': 'zh', 'target': 'en'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

