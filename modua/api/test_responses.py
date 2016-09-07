from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from .models import User, Language, Word, Definition


class DefinitionDetailTestCase(APITestCase):

    def setUp(self):
        english = Language.objects.create(language='en')
        self.spanish = Language.objects.create(language='es')
        john = User.objects.create_user(username='john', email='jdoe@gmail.com', password='password')
        self.word = Word.objects.create(word='foo', owner=john, language=english)
        Definition.objects.create(
            word=self.word,
            language=self.spanish,
            definition='bar',
            owner=john
        )
        self.client = APIClient()
        self.client.login(username='john', password='password')
        self.url = reverse('definition-detail', kwargs={'definition': 'bar', 'word': 'foo', 'language': 'en'})

    def test_get_definition(self):
        kwargs= {'definition': 'bar', 'word': 'foo', 'language': 'en', 'target': 'es', 'username': 'john'}
        response = self.client.get(self.url, kwargs)
        self.assertContains(response, 'bar')

    def test_delete_definition(self):
        kwargs= {'definition': 'bar', 'word': 'foo', 'language': 'en', 'target': 'es', 'username': 'john'}
        response = self.client.delete(self.url, kwargs)
        queryset = Definition.objects.all()
        self.assertQuerysetEqual(queryset, [])

    def test_can_not_delete_public(self):
        Definition.objects.create(
            word=self.word,
            language=self.language,
            definition='public',
        )
        kwargs= {'definition': 'public', 'word': 'foo', 'language': 'en', 'target': 'es', 'username': 'john'}
        response = self.client.delete(self.url, kwargs)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class TestViews(APITestCase):


    def setUp(self):
        for chinese, english in [("我", "I"), ("爱", "love"), ("中国", "China")]:
            Word.create(word=chinese, language='zh', definition=english, definition_language='en')
        User.objects.create_user('john', 'john@gmail.com', 'password')


    def test_search_status_code_200(self):
        '''
        Passes if a valid search returns a status code of 200.
        '''
        Word.create(word='hello', language='en', definition='a greeating', definition_language='zh')
        response = self.client.get("/api/0.1/languages/en/hello/")
        self.assertEqual(response.status_code, 200)

    def test_term_search(self):
        '''
        Passes if the json returned from a valid request is the correct json.
        '''
        Word.create(word='hello', language='en', definition='a greeating', definition_language='zh')
        response = self.client.get("/api/0.1/languages/en/hello/")
        self.assertContains(response, 'hello')

    def test_bad_term_search(self):
        '''
        Passes if a request for a word not in the dictionary returns a status code 404.
        '''
        response = self.client.get("/api/0.1/languages/en/term_not_in_DB/", format='json')
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
        response = self.client.get("/api/0.1/languages/zh/term_not_in_DB/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestLanguageAPI(APITestCase):


    def test_language_list_one_language(self):
        '''
        Passes if /languages/ returns the correct json.
        '''
        Language.objects.create(language='en')
        response = self.client.get("/api/0.1/languages/", format='json')
        json = response.json()
        results = json['results']
        expected = {'language': 'en'}
        for d in results:
            self.assertTrue(d['language'] == expected['language'])
