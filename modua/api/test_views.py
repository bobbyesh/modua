from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate, APIClient
from rest_framework.authtoken.models import Token
from mock import patch
from django.core.urlresolvers import reverse

from .serializers import PublicDefinitionSerializer
from .models import PublicDefinition, User, PublicWord, UserDefinition, UserWord
from .views import ParseView, PublicArticleView


DEBUG = True


class UserTestMixin(object):

    def setUp(self):
        self.user = User.objects.create(username='john', password='password')
        token = Token.objects.get(user__username='john')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)



class PublicDefinitionListViewTestCase(APITestCase):

    def setUp(self):
        self.word = PublicWord.objects.create(word='foo')
        definition = PublicDefinition.objects.create(word=self.word, definition='bar')
        self.client = APIClient()

    def test_read(self):
        url = reverse('public-definition-list', kwargs={'word': 'foo'})
        response = self.client.get(url)
        self.assertContains(response, 'foo')

    def test_returns_two_definitions(self):
        definition = PublicDefinition.objects.create(word=self.word, definition='meso')
        data = {'word': 'foo'}
        url = reverse('public-definition-list', kwargs=data)
        response = self.client.get(url, data={'word': 'foo'})
        self.assertContains(response, str(definition.definition))
        self.assertContains(response, 'bar')

    def test_bad_word_returns_empty(self):
        data = {'word': 'not_in_db'}
        url = reverse('public-definition-list', kwargs=data)
        response = self.client.get(url, data)
        results = response.data['results']
        self.assertEqual(results, [])


class UserDefinitionListViewTestCase(UserTestMixin, APITestCase):
    """Tests that the UserDefinitionListView and 'user-definition-list' URL route are
    working correctly.

    The view only supports the GET method.

    """

    def setUp(self):
        super().setUp()
        word = UserWord.objects.create(word='foo', owner=self.user)
        definition = UserDefinition.objects.create(owner=self.user, word=word, definition='bar')

    def test_read(self):
        url = reverse('user-definition-list', kwargs={'word': 'foo'})
        response = self.client.get(url)
        self.assertContains(response, 'foo')

    def test_invalid_word_returns_empty(self):
        data = {'word': 'notindb'}
        url = reverse('user-definition-list', kwargs=data)
        response = self.client.get(url, data)
        results = response.data['results']
        self.assertEqual(results, [])


class UserDefinitionCreateDestroyViewTestCase(UserTestMixin, APITestCase):

    def setUp(self):
        super().setUp()

    def test_no_duplicate(self):
        word = UserWord.objects.create(word='foo', owner=self.user)
        definition = UserDefinition.objects.create(owner=self.user, word=word, definition='bar')
        url = reverse('user-definition-create-destroy', kwargs={'word': 'foo'})
        response = self.client.post(url, {'definition': 'bar'})
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        UserWord.objects.create(word='foo', owner=self.user)
        url = reverse('user-definition-create-destroy', kwargs={'word': 'foo'})
        response = self.client.post(url, {'definition': 'bar'})

        queryset = UserDefinition.objects.filter(owner=self.user, definition='bar')
        self.assertTrue(len(queryset) == 1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


class UserWordDetailTestCase(UserTestMixin, APITestCase):

    def setUp(self):
        super().setUp()

    def test_create(self):
        url = reverse('user-word-detail', kwargs={'word': 'foo'})
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        queryset = UserWord.objects.filter(owner=self.user, word='foo')
        self.assertTrue(len(queryset) == 1)
        self.assertTrue(str(queryset[0].word) == 'foo')


    def test_delete(self):
        word = UserWord.objects.create(word='foo', owner=self.user)
        url = reverse('user-word-detail', kwargs={'word': 'foo'})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_no_duplicate(self):
        url = reverse('user-word-detail', kwargs={'word': 'foo'})
        response = self.client.post(url)
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        word = UserWord.objects.create(word='foo', owner=self.user)
        url = reverse('user-word-detail', kwargs={'word': 'foo'})
        response = self.client.patch(url, {'ease': 'hard'})
        queryset = UserWord.objects.filter(owner=self.user, word='foo')
        self.assertTrue(str(queryset[0].ease) == 'hard')

    def test_put_not_allowed(self):
        url = reverse('user-word-detail', kwargs={'word': 'foo'})
        response = self.client.put(url, {'ease': 'hard'})
        self.assertTrue(response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED)


class PublicWordListTestCase(APITestCase):
    def setUp(self):
        word = PublicWord.objects.create(word='foo')

    def test_read(self):
        self.client = APIClient()
        url = reverse('public-word-list')
        response = self.client.get(url)
        self.assertContains(response, 'foo')


class ParseViewTestCase(APITestCase):

    def test_parse(self):
        factory = APIRequestFactory()
        url = reverse('parse')
        request = factory.post(url, data={'string': '我是美国人'})
        response = ParseView.as_view()(request)
        self.assertTrue(x['string'] in {'我','是', '美国人'} for x in response.data)

class PublicArticleViewTestCase(APITestCase):
    def setUp(self):
        word = PublicWord.objects.create(word='你好', pinyin='nǐ hǎo')
        definition = PublicDefinition.objects.create(definition='hello', word=word)

        factory = APIRequestFactory()
        url = reverse('public-article')
        data = {
            'text': '    你好！\n   你好！',
            'title': '你好',
        }
        request = factory.post(url, data=data)
        self.response = PublicArticleView.as_view()(request)
        self.expected = {
            'title': [
                    {
                        'word': '你好',
                        'index': 0,
                        'pinyin': 'nǐ hǎo',
                        'definition': ['hello']
                    },
            ],
            'paragraphs': [
                [
                    {
                        'word': '你好',
                        'index': 0,
                        'pinyin': 'nǐ hǎo',
                        'definition': ['hello']
                    },
                    {
                        'word': '！', # Chinese exclamation point
                        'index': 1,
                        'pinyin': '',
                        'definition': '',
                    }
                ],
                [
                    {
                        'word': '你好',
                        'index': 0,
                        'pinyin': 'nǐ hǎo',
                        'definition': ['hello']
                    },
                    {
                        'word': '！', # Chinese exclamation point
                        'index': 1,
                        'pinyin': '',
                        'definition': '',
                    },
                ]
            ]
        }

    def test_article_returns_with_paragraphs(self):
        paragraphs = self.response.data['paragraphs']
        self.assertEqual(len(paragraphs), 2)

    def test_words(self):
        paragraphs = self.response.data['paragraphs']
        result = set(word['word'] for paragraph in paragraphs for word in paragraph)
        expected = set(word['word'] for paragraph in self.expected['paragraphs'] for word in paragraph)
        self.assertEqual(result, expected)

    def test_title_word(self):
        result = self.response.data['title'][0]['word']
        expected = self.expected['title'][0]['word']
        self.assertEqual(result, expected)
