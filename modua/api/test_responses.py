from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from .models import User, PublicWord, PublicDefinition


class PublicDefinitionDetailTestCase(APITestCase):

    def setUp(self):
        john = User.objects.create_user(username='john', email='jdoe@gmail.com', password='password')
        word = PublicWord.objects.create(word='foo')
        PublicDefinition.objects.create(
            word=word,
            definition='bar',
            owner=john
        )
        self.word = word
        self.client = APIClient()
        self.client.login(username='john', password='password')

    def test_get_definition(self):
        url = reverse('definition-detail', kwargs={'definition': 'bar', 'word': 'foo'})
        kwargs= {'definition': 'bar', 'word': 'foo', 'username': 'john'}
        response = self.client.get(url, kwargs)
        self.assertContains(response, 'bar')

    def test_delete_definition(self):
        url = reverse('definition-detail', kwargs={'definition': 'bar', 'word': 'foo'})
        kwargs= {'definition': 'bar', 'word': 'foo', 'username': 'john'}
        response = self.client.delete(url, kwargs)
        queryset = PublicDefinition.objects.all()
        self.assertQuerysetEqual(queryset, [])

    def test_can_not_delete_public(self):
        PublicDefinition.objects.create(
            word=self.word,
            definition='public',
        )

        kwargs= {'definition': 'public', 'word': 'foo', 'username': 'john'}
        url = reverse('definition-detail', kwargs={'definition': 'public', 'word': 'foo'})
        response = self.client.delete(url, kwargs)

        result = PublicDefinition.objects.filter(
            word=self.word,
            definition='public',
        )

        self.assertTrue(len(result) != 0)


class TestPublicRequests(APITestCase):

    def setUp(self):
        for chinese_word, english_word in [("我", "I"), ("爱", "love"), ("中国", "China")]:
            word = PublicWord.objects.create(word=chinese_word)
            definition = PublicDefinition.objects.create(definition=english_word, word=word)


    def test_search_status_code_200(self):
        '''
        Passes if a valid search returns a status code of 200.
        '''
        response = self.client.get("/api/0.1/word/我/")
        self.assertEqual(response.status_code, 200)

    def test_term_search(self):
        '''
        Passes if the json returned from a valid request is the correct json.
        '''
        response = self.client.get("/api/0.1/word/我/")
        self.assertContains(response, '我')

    def test_bad_term_search(self):
        '''
        Passes if a request for a word not in the dictionary returns a status code 404.
        '''
        response = self.client.get("/api/0.1/word/term_not_in_DB/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_url(self):
        '''
        Passes if an invalid url returns a 404 response.
        '''
        response = self.client.get("/api/badurl/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_nondelimited_search(self):
        '''
        Passes if a request for a nondelimited word that isn't in the database returns a 404 response.
        '''
        response = self.client.get("/api/0.1/word/term_not_in_DB/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
