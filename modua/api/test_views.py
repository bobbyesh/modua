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

class ArticleView(APITestCAse):
    def setUp(self):
        PublicWord.objects.create(word='你好', pinyin='‘nǐ hǎo’', definition='hello')
        factory = APIRequestFactory()
        url = reverse('article')
        data = {
            'text': '    你好！\n   你好！',
            'title': '你好',
        }
        request = factory.post(url, data=data)
        self.response = ArticleView.as_view()(request)
        self.expected = {
            'title': [
                    {
                        'headword': '你好'
                        'id': 0,
                        'pinyin': ‘nǐ hǎo’,
                        'definition': 'hello'
                    },
            ],
            'paragraphs':
                [
                    {
                        'headword': '你好'
                        'id': 0,
                        'pinyin': ‘nǐ hǎo’,
                        'definition': 'hello'
                    },
                    {
                        'headword': '!',
                        'id': 1,
                        'pinyin': ‘’,
                        'definition': ''
                ],
                [
                    {
                        'headword': '你好'
                        'id': 0,
                        'pinyin': ‘nǐ hǎo’,
                        'definition': 'hello'
                    },
                    {
                        'headword': '!',
                        'id': 1,
                        'pinyin': ‘’,
                        'definition': ''
                ],
        }

    def test_article_returns_with_paragraphs(self):
        paragraphs = self.response.data['paragraphs']
        self.assertEqual(len(paragraphs), 2)

    def test_headwords(self):
        paragraphs = self.response.data['paragraphs']
        result = set(p['headword'] for p in paragraphs)
        expected = set(p['headword'] for p in self.expected['paragraphs'])
        self.assertEqual(result, expected)

    def test_title_headword(self):
        result = self.response.data['title'][0]['headword']
        expected = self.response.data['expected'][0]['headword']
        self.assertEqual(result, expected)
