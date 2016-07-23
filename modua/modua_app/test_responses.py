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



class TestViews(APITestCase):


    def setUp(self):
        eng = Languages.objects.create(language='en')
        zh = Languages.objects.create(language='zh')

        Definitions.objects.create(word="hello",
                                           definition="A greeting",
                                           language=eng)

        Definitions.objects.create(word='kool-aid',
                                   definition='the koolest drink ever',
                                   language=zh)

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
        response = self.client.get("/api/0.1/languages/en/hello", format='json')
        json = response.json()[0]
        self.assertEqual(json, {'word': "hello",
                                    'definition': 'A greeting',
                                    'transliteration': None })
    
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
        Passes if a the json returned from a valid search for a nondelimited word is correct.
        '''
        response = self.client.get("/api/0.1/languages/zh/kool-aidxxxx", format='json')
        json = response.json()[0]
        self.assertDictEqual(json, {'word': 'kool-aid',
                                    'definition': 'the koolest drink ever',
                                    'transliteration': None
                               })

    def test_bad_nondelimited_search(self):
        '''
        Passes if a request for a nondelimited word that isn't in the database returns a 404 response.
        '''
        response = self.client.get("/api/0.1/languages/zh/term_not_in_DB", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_language_list_one_language(self):
        '''
        Passes if /languages/ returns the correct json.
        '''
        Languages.objects.create(language='en')
        response = self.client.get("/api/0.1/languages/", format='json')
        json = response.json()[0]
        self.assertEqual(json, {'language': 'en'})


    def test_language_list_two_languages(self):
        '''
        Passes if /languages/ returns the correct json.
        '''
        Languages.objects.create(language='en')
        Languages.objects.create(language='zh')
        response = self.client.get("/api/0.1/languages/", format='json')
        json = response.json()[0]
        self.assertDictEqual(json, {'language': 'en'},
                                {'language': 'zh'})
