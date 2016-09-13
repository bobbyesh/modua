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
        self.en = Language.objects.create(language='en')
        self.word = PublicWord.objects.create(word='foo', language=self.en)
        definition = PublicDefinition.objects.create(word=self.word, language=self.en, definition='bar')
        self.client = APIClient()

    def test_read(self):
        url = reverse('public-definition-list', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.get(url)
        self.assertContains(response, 'foo')

    def test_returns_two_definitions(self):
        definition = PublicDefinition.objects.create(word=self.word, language=self.en, definition='meso')
        url = reverse('public-definition-list', kwargs={'language': 'en', 'word': 'foo'})
        response = self.client.get(url)
        self.assertContains(response, str(definition.definition))
        self.assertContains(response, 'bar')

    def test_bad_language_returns_empty(self):
        url = reverse('public-definition-list', kwargs={'language': 'zh', 'word': 'foo'})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(results, [])

    def test_bad_word_returns_empty(self):
        url = reverse('public-definition-list', kwargs={'language': 'en', 'word': 'not_in_db'})
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

    def test_invalid_word_returns_empty(self):
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


class ParseViewTestCase(APITestCase):

    def test_parse(self):
        factory = APIRequestFactory()
        url = reverse('parse')
        request = factory.post(url, data={'string': '我是美国人', 'language': 'zh'})
        response = ParseView.as_view()(request)
        self.assertTrue(x['string'] in {'我','是', '美国人'} for x in response.data)

"""
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

"""
