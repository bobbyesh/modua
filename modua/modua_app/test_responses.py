import json
from collections import OrderedDict
from django.core.urlresolvers import reverse
from django.utils.six import BytesIO
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.parsers import JSONParser

from .models import Definitions, User, Languages
from .views import LanguageWordlistView
from .serializers import LanguagesSerializer, DefinitionsSerializer

import pdb


class TestViews(APITestCase):


    def setUp(self):
        self.eng = Languages.objects.create(language='en')
        self.zh = Languages.objects.create(language='zh')

        Definitions.objects.create(word="hello",
                                           definition="A greeting",
                                           language=self.eng)


        User.objects.create_user('john', 'john@gmail.com', 'password')


    def test_search_status_code_200(self):
        '''
        Passes if a valid search returns a status code of 200.
        '''
        response = self.client.get("/api/0.1/languages/en/hello", format='json')
        self.assertEqual(response.status_code, 200)

    def test_term_search(self):
        '''
        Passes if the json returned from a valid request is the correct json.
        '''
        response = self.client.get("/api/0.1/languages/en/hello")
        json = response.json()
        results = json['results']
        for result in results:
            self.assertEqual(result['word'], 'hello')

    def test_bad_term_search(self):
        '''
        Passes if a request for a word not in the dictionary returns a status code 404.
        '''
        response = self.client.get("/api/0.1/languages/en/term_not_in_DB", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_url(self):
        '''
        Passes if an invalid url returns a 404 response.
        '''
        response = self.client.get("/api/badurl", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nondelimited_term_search(self):
        '''
        Passes if the json returned from a valid search for a nondelimited word is correct.
        '''
        tokens = {'㚻', '一派謊言', '一眨眼', '一派'}
        for word in tokens:
            Definitions.objects.create(
                word=word,
                definition='foo',
                language=self.zh
            )

        queryset = Definitions.objects.filter(language=self.zh)
        self.assertTrue(len(queryset) == len(tokens))

        concat = ''.join(t for t in tokens)
        response = self.client.get("/api/0.1/languages/zh/" + concat, format='json')
        json = response.json()
        results = json['results']
        token_in_json = False
        for obj in results:
            if 'word' in obj:
                self.assertTrue(obj['word'] in tokens)


    def test_bad_nondelimited_search(self):
        '''
        Passes if a request for a nondelimited word that isn't in the database returns a 404 response.
        '''
        response = self.client.get("/api/0.1/languages/zh/term_not_in_DB", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestLanguageAPI(APITestCase):


    def test_language_list_one_language(self):
        '''
        Passes if /languages/ returns the correct json.
        '''
        Languages.objects.create(language='en')
        response = self.client.get("/api/0.1/languages/", format='json')
        json = response.json()
        results = json['results']
        expected = {'language': 'en'}
        for d in results:
            self.assertTrue(d['language'] == expected['language'])


    def test_language_list_two_languages(self):
        '''
        Passes if /languages/ returns the correct json.
        '''
        Languages.objects.create(language='en')
        Languages.objects.create(language='zh')
        response = self.client.get("/api/0.1/languages/", format='json')
        json = response.json()
        results = json['results']
        results = sorted(results, key=lambda x: x['language'])
        expected = [{'language': 'en'}, {'language': 'zh'}]
        expected = sorted(expected, key=lambda x: x['language'])
        for x,y in zip(results, expected):
            self.assertTrue(x['language'] == y['language'])
