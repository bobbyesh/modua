from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate, APIClient
from rest_framework.authtoken.models import Token
from mock import patch
from django.core.urlresolvers import reverse

from .serializers import DefinitionSerializer
from .models import Definition, User, Language, Word
from .views import LanguageListView, DefinitionListView, AnnotationView, URLImportView, WordDetailView

DEBUG = True

class WordDetailTestCase(APITestCase):

    def setUp(self):
        Language.objects.create(language='en')
        Language.objects.create(language='es')
        Language.objects.create(language='zh')
        john = User.objects.create_user(username='john', email='jdoe@gmail.com', password='password')
        self.johns_token = Token.objects.create(user=john)
        sally = User.objects.create_user(username='sally', email='sally@gmail.com', password='password')
        word = Word.create('hey', 'en')
        word.add_definition('hola', 'es')
        word.set_user(username='john')

        self.john = john
        self.sally = sally
        self.client = APIClient()
        self.client.login(username='john', password='password')

    def test_update_ease(self):
        url = reverse('word-detail', kwargs={'language': 'en', 'word': 'hey'})
        response = self.client.patch(url, {'username': 'john', 'ease': 'easy'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'easy')

        actual_ease = self.john.word_set.filter(word='hey')[0].ease
        self.assertEqual('easy', str(actual_ease))


    def test_does_contain_word(self):
        w = Word.create('cool', 'en')
        w.add_definition('not hot', 'zh')
        self.view = WordDetailView.as_view()
        self.factory = APIRequestFactory()
        request = self.factory.get('/api/0.1/languages/en/cool/')
        self.response = self.view(request, language='en', word='cool')
        self.assertContains(self.response, 'cool')

    def test_wrong_language_raises_404(self):
        w = Word.create('cool', 'en')
        w.add_definition('not hot', 'zh')

        self.view = WordDetailView.as_view()
        self.factory = APIRequestFactory()
        kwargs={'language': 'zh', 'word': 'cool'}
        url = reverse('word-detail', kwargs=kwargs) 
        print(url)
        response = self.client.get(url, kwargs)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_word_raises_404(self):
        w = Word.create('cool', 'en')
        w.add_definition('not hot', 'zh')
        self.view = WordDetailView.as_view()
        self.factory = APIRequestFactory()
        request = self.factory.get('/api/0.1/languages/en/basketball/')
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
        Language.objects.create(language='en')
        Language.objects.create(language='es')
        Language.objects.create(language='zh')
        john = User.objects.create_user(username='john', password='password')
        sally = User.objects.create_user(username='sally', password='password')

        word = Word.create('hey', 'en')
        word.add_definition('hola', 'es')
        word.add_definition('es una blah', 'es')
        word.add_definition('ni hao', 'zh')
        word.user = john
        word.save()

        sallys_word = Word.objects.create(
            word='hey',
            language=Language.objects.get(language='en'),
            user=sally
        )

        sallys_word.add_definition('special definition', 'zh')

        self.client = APIClient()
        self.client.login(username='john', password='password')

    def test_definition_list(self):
        kwargs={'language': 'en', 'word': 'hey'}
        url = reverse('definition-list', kwargs=kwargs)
        response = self.client.get(url, {'target': 'es'})

        if DEBUG:
            print('test_definition_list')
            print(url)
            print(response.data)
            print()

        self.assertContains(response, 'hola')
        self.assertContains(response, 'es una blah')
        self.assertNotContains(response, 'ni hao')

    def test_filter_by_user(self):
        kwargs={'language': 'en', 'word': 'hey'}
        url = reverse('definition-list', kwargs=kwargs)
        kwargs['username'] = 'john'
        response = self.client.get(url, kwargs)

        if DEBUG:

            print("kwargs = {}".format(kwargs))
            print(url)
            print(response.data)
            print()
            import pdb;pdb.set_trace()

        self.assertContains(response, 'hola')
        self.assertContains(response, 'es una blah')
        self.assertContains(response, 'ni hao')
        self.assertNotContains(response, 'special definition')


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
