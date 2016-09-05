from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from mock import patch

from .serializers import DefinitionSerializer
from .models import Definition, User, Language, Word
from .views import LanguageListView, DefinitionListView, DefinitionDetailView, AnnotationView, URLImportView, UpdateWordView, WordDetailView


class WordDetailTestCase(APITestCase):

    def test_update_ease(self):
        self.password = 'password'
        self.username = 'john'
        self.user = User.objects.create(username=self.username, email='jdoe@gmail.com', password=self.password)
        self.word = Word.create(word='hey', language='en', definition='hola', definition_language='es', ease='hard')
        self.word.users.add(self.user)
        self.token = Token.objects.create(user=self.user)
        factory = APIRequestFactory()
        expected_ease = 'easy'
        request_url = '/api/0.1/language/{}/word/{}?&username={}&password={}&ease={}'.format(
            'en',
            self.word,
            self.username,
            self.password,
            expected_ease
        )
        kwargs = {
            'language': 'en',
            'word': self.word,
            'username': self.username,
            'password': self.password,
            'ease': expected_ease
        }

        request = factory.patch(
            request_url,
            kwargs
        )
        force_authenticate(request, self.user, self.token)
        response = UpdateWordView.as_view()(request)

        resulting_ease = self.user.word_set.filter(word=self.word)[0].ease

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, expected_ease)
        self.assertEqual(expected_ease, str(resulting_ease))

    def test_does_contain_word(self):
        Word.create(
            language='en',
            word='cool',
            definition_language='zh',
            definition='not hot',
        )
        self.view = WordDetailView.as_view()
        self.factory = APIRequestFactory()
        request = self.factory.get('/api/0.1/languages/en/cool/')
        self.response = self.view(request, language='en', word='cool')
        self.assertContains(self.response, 'cool')

    def test_wrong_language_raises_404(self):
        Word.create(
            language='en',
            word='cool',
            definition_language='zh',
            definition='not hot',
        )
        self.view = WordDetailView.as_view()
        self.factory = APIRequestFactory()
        request = self.factory.get('/api/0.1/languages/zh/cool/')
        response = self.view(request, language='zh', word='cool')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_word_raises_404(self):
        Word.create(
            language='en',
            word='cool',
            definition_language='zh',
            definition='not hot',
        )
        self.view = WordDetailView.as_view()
        self.factory = APIRequestFactory()
        request = self.factory.get('/api/0.1/languages/en/basketball/3/')
        response = self.view(request, language='en', word='basketball')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class URLImportTestCase(APITestCase):

    def setUp(self):
        Language.objects.create(language='zh')
        self.user = User.objects.create(username='johndoe', email='jdoe@gmail.com', password='password')
        self.token = Token.objects.create(user=self.user)

    def test_url_import_response_200(self):
        request = self.get_request()
        response = URLImportView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_url_multiple_fetch_200(self):
        request = self.get_request()
        URLImportView.as_view()(request)

        request = self.get_request()
        response = URLImportView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def get_request(self):
        factory = APIRequestFactory()
        url = 'http://www.fox2008.cn/Article/2009/20090406192831_21829.html'
        request_url = '/api/0.1/import?url={}&language=zh'.format(url)
        request = factory.post(request_url, {'url': url, 'language': 'zh'})
        force_authenticate(request, user=self.user, token=self.token.key)
        return request

    def test_wrong_language_response_is_404(self):
        factory = APIRequestFactory()
        url = 'http://www.fox2008.cn/Article/2009/20090406192831_21829.html'
        request_url = '/api/0.1/import?url={}&language=foo'.format(url)
        request = factory.post(request_url, {'url': url, 'language': 'foo'})
        force_authenticate(request, user=self.user, token=self.token.key)
        response = URLImportView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateWordTestCase(APITestCase):

    def setUp(self):
        self.password = 'password'
        self.username = 'john'
        self.user = User.objects.create(username=self.username, email='jdoe@gmail.com', password=self.password)
        self.word = Word.create(word='hey', language='en', definition='hola', definition_language='es', ease='hard')
        self.word.users.add(self.user)
        self.token = Token.objects.create(user=self.user)

    def test_update_ease(self):
        factory = APIRequestFactory()
        expected_ease = 'easy'
        request_url = '/api/0.1/language/{}/word/{}?&username={}&password={}&ease={}'.format(
            'en',
            self.word,
            self.username,
            self.password,
            expected_ease
        )
        kwargs = {
            'language': 'en',
            'word': self.word,
            'username': self.username,
            'password': self.password,
            'ease': expected_ease
        }

        request = factory.patch(
            request_url,
            kwargs
        )
        force_authenticate(request, self.user, self.token)
        response = UpdateWordView.as_view()(request)

        resulting_ease = self.user.word_set.filter(word=self.word)[0].ease

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, expected_ease)
        self.assertEqual(expected_ease, str(resulting_ease))


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
        Word.create(
            word='cool',
            language='en',
            definition_language='es',
            definition='not hot',
        )

        Word.create(
            language='en',
            word='building',
            definition_language='es',
            definition='a thing in cities',
        )

        chinese = Language.objects.create(language='zh')

        Word.create(
            word='chineseword',
            language='zh',
            definition_language='zh',
            definition='some translation',
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
        Word.create(
            language='en',
            word='cool',
            definition_language='zh',
            definition='not hot',
        )
        self.view = DefinitionDetailView.as_view()
        self.factory = APIRequestFactory()

    def test_does_contain_word(self):
        id = Word.objects.get(word='cool').id
        id = str(id)
        request = self.factory.get('/api/0.1/languages/en/cool/1/')
        self.response = self.view(request, language='en', word='cool', id=id)
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


'''
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
        serialized = []
        for t in tokens:
            qset = Definition.objects.filter(word=t, language=language, target=target)
            serializer = DefinitionSerializer(qset, many=True)
            serialized.append(serializer.data)

        return serialized


    def test_empty_query_returns_404(self):
        url = '/api/0.1/annotate/?string&language=zh&target=en'
        request = self.factory.post(url, {'string': '', 'language': 'zh', 'target': 'en'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

'''
