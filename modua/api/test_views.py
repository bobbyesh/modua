from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate, APIClient
from rest_framework.authtoken.models import Token
from mock import patch
from django.core.urlresolvers import reverse

from .serializers import PublicDefinitionSerializer
from .models import PublicDefinition, User, Language, PublicWord, UserDefinition, UserWord
from .views import ParseView


DEBUG = True


class UserTestMixin(object):

    def setUp(self):
        self.user = User.objects.create(username='john', password='password')
        token = Token.objects.get(user__username='john')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class PublicDefinitionListViewTestCase(APITestCase):

    def setUp(self):
        en = Language.objects.create(language='en')
        word = PublicWord.objects.create(word='foo', language=en)
        definition = PublicDefinition.objects.create(word=word, language=en, definition='bar')
        self.client = APIClient()

    def test_read(self):
        url = reverse('public-definition-list', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.get(url)
        self.assertContains(response, 'foo')
    
    def test_bad_language_returns_empty(self):
        url = reverse('public-definition-list', kwargs={'language': 'zh', 'word': 'foo'})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(results, [])

    def test_word_language_returns_empty(self):
        url = reverse('public-definition-list', kwargs={'language': 'en', 'word': 'not in db'})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(results, [])


class UserDefinitionListViewTestCase(UserTestMixin, APITestCase):
    """Tests that the UserDefinitionListView and 'user-definition-list' URL route are
    working correctly.

    The view only supports the GET method.

    """

    def setUp(self):
        super().setUp()
        en = Language.objects.create(language='en')
        word = UserWord.objects.create(word='foo', language=en, owner=self.user)
        definition = UserDefinition.objects.create(owner=self.user, word=word, language=en, definition='bar')

    def test_read(self):
        url = reverse('user-definition-list', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.get(url)
        self.assertContains(response, 'foo')

    def test_bad_language_returns_empty(self):
        url = reverse('user-definition-list', kwargs={'language': 'zh', 'word': 'foo'})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(results, [])

    def test_invalid_language_returns_empty(self):
        url = reverse('user-definition-list', kwargs={'language': 'en', 'word': 'notindb'})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(results, [])


class UserDefinitionCreateDestroyViewTestCase(UserTestMixin, APITestCase):

    def setUp(self):
        super().setUp()

    def test_no_duplicate(self):
        en = Language.objects.create(language='en')
        word = UserWord.objects.create(word='foo', language=en, owner=self.user)
        definition = UserDefinition.objects.create(owner=self.user, word=word, language=en, definition='bar')
        url = reverse('user-definition-create-destroy', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.post(url, {'definition': 'bar', 'target': 'en'})
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        en = Language.objects.create(language='en')
        UserWord.objects.create(word='foo', language=en, owner=self.user)
        url = reverse('user-definition-create-destroy', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.post(url, {'definition': 'bar', 'target': 'en'})

        queryset = UserDefinition.objects.filter(owner=self.user, definition='bar')
        self.assertTrue(len(queryset) == 1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    
    def test_bad_language_should_return_404(self):
        url = reverse('user-definition-create-destroy', kwargs={'language': 'zh', 'word': 'foo'})
        response = self.client.post(url, {'ease': 'hard'})
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)




class UserWordDetailTestCase(UserTestMixin, APITestCase):

    def setUp(self):
        super().setUp()
        self.en = Language.objects.create(language='en')

    def test_create(self):
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        queryset = UserWord.objects.filter(owner=self.user, word='foo')
        self.assertTrue(len(queryset) == 1)
        self.assertTrue(str(queryset[0].word) == 'foo')


    def test_delete(self):
        word = UserWord.objects.create(word='foo', language=self.en, owner=self.user)
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_no_duplicate(self):
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.post(url)
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        word = UserWord.objects.create(word='foo', language=self.en, owner=self.user)
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.patch(url, {'ease': 'hard'})
        queryset = UserWord.objects.filter(owner=self.user, word='foo')
        self.assertTrue(str(queryset[0].ease) == 'hard')

    def test_put_not_allowed(self):
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.put(url, {'ease': 'hard'})
        self.assertTrue(response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_bad_language_should_return_404(self):
        url = reverse('user-word-detail', kwargs={'language': 'zh', 'word': 'foo'})
        response = self.client.post(url, {'ease': 'hard'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PublicWordListTestCase(APITestCase):
    def setUp(self):
        self.en = Language.objects.create(language='en')
        word = PublicWord.objects.create(word='foo', language=self.en)

    def test_read(self):
        self.client = APIClient()
        url = reverse('public-word-list', kwargs={'language': 'en'})
        response = self.client.get(url)
        self.assertContains(response, 'foo')


'''
class ParseViewTestCase(APITestCase):

    def test_parse(self):
        factory = APIRequestFactory()
        url = reverse('parse', kwargs={'language':'zh'})
        request = factory.post(url, {'string': '我是美国人'})
        response = ParseView.as_view()(request)
        self.assertTrue(x['string'] in {'我','是', '美国人'} for x in response.data)
'''

'''

class UserWordDetailTestCase(APITestCase):
    """
    An authenticated user can read a word, create a word, delete a word,
    or modify a word's ease.

    """

    def setUp(self):
        self.john = User.objects.create(username='john', password='password')
        self.en = Language.objects.create(language='en')
        self.client = APIClient()
        token = Token.objects.get(user__username='john')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create(self):
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.post(url, {'ease': 'easy'})
        queryset = Word.objects.filter(owner__username='john')
        self.assertTrue(len(queryset) == 1)

    def test_read(self):
        Word.objects.create(word='foo', language=self.en, owner=self.john)
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.get(url)
        self.assertContains(response, 'foo')

    def test_modify(self):
        Word.objects.create(word='foo', language=self.en, owner=self.john, ease='easy')
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.patch(url, {'ease': 'hard'})

        queryset = Word.objects.filter(word='foo', owner=self.john)
        instance = Word.objects.filter(word='foo', owner=self.john)[0]
        dummy = Word.objects.create(word='dummy', ease='hard', language=self.en)
        self.assertEqual(len(queryset), 1)
        self.assertEqual(instance.ease, dummy.ease)

    def test_put(self):
        Word.objects.create(word='foo', language=self.en, owner=self.john, ease='easy')
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.put(url, {'language': 'en', 'word': 'foo', 'ease': 'hard'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        Word.objects.create(word='foo', language=self.en, owner=self.john)
        url = reverse('user-word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.delete(url)
        queryset = Word.objects.filter(word='foo', language=self.en, owner=self.john)
        self.assertTrue(len(queryset) == 0)

    """

    .. todo:  Test that this view doesn't fetch public definitions.

    """


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

    def test_update_ease(self):
        token = Token.objects.get(user__username='john')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('word-detail', kwargs={'language': 'en', 'word': 'hey'})
        response = self.client.patch(url, {'username': 'john', 'ease': 'easy'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'easy')

        actual_ease = self.john.api_word_owner.filter(word='hey')[0].ease
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
        en = Language.objects.create(language='en')
        Language.objects.create(language='es')
        Language.objects.create(language='zh')
        john = User.objects.create_user(username='john', password='password')
        sally = User.objects.create_user(username='sally', password='password')

        word = Word.create('hey', 'en')
        word.add_definition('hola', 'es')
        word.add_definition('es una blah', 'es')
        word.add_definition('ni hao', 'zh')
        definition = Definition.objects.create(word=word, definition='foo bar', language=en, owner=john)
        word.owner = john
        word.save()

        sallys_word = Word.objects.create(
            word='hey',
            language=Language.objects.get(language='en'),
            owner=sally
        )

        sallys_word.add_definition('special definition', 'zh')
        self.john = john
        self.client = APIClient()

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
        token = Token.objects.create(user=self.john)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        kwargs={'language': 'en', 'word': 'hey'}
        url = reverse('definition-list', kwargs=kwargs)
        response = self.client.get(url)

        if DEBUG:

            print("kwargs = {}".format(kwargs))
            print(url)
            print(response.data)
            print()

        self.assertContains(response, 'foo')
        self.assertNotContains(response, 'es una blah')
        self.assertNotContains(response, 'ni hao')
        self.assertNotContains(response, 'special definition')




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
