from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json

from .models import Definitions



class TestViews(APITestCase):

    text = "hello"
    valid_lang = "en-US"
    invalid_lang = "blah-lang"
    url_one_word = "/api/0.1/search/en-US/hello"
    url_search = "/api/0.1/search/en-US/"
    url_nondelimited_word = "/api/0.1/search/zh-Hant/kool-aidxxxx"
    nondelimited_url = "/api/0.1/search/zh-Hant/"
    definition = "A greeting"

    def setUp(self):
        Definitions.objects.create(word_character=self.text,
                                           definition=self.definition)
        Definitions.objects.create(word_character='kool-aid',
                                   definition='the koolest drink ever')

    def test_search_status_code_200(self):
        '''
        Passes if a valid search returns a status code of 200.
        '''
        response = self.client.get(self.url_one_word, format='json')
        self.assertEqual(response.status_code, 200)

    def test_term_search(self):
        '''
        Passes if the json returned from a valid request is the correct json.
        '''
        response = self.client.get(self.url_one_word, format='json')
        json = response.json()
        self.assertEqual(json, {'word_character': self.text,
                                    'definition': self.definition,
                                    'transliteration': None })
    
    def test_bad_term_search(self):
        '''
        Passes if a request for a word not in the dictionary returns a status code 404.
        '''
        response = self.client.get(self.url_search + "term_not_in_DB", format='json')
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
        response = self.client.get(self.url_nondelimited_word, format='json')
        json = response.json()
        self.assertEqual(json, {'word_character': 'kool-aid',
                                    'definition': 'the koolest drink ever',
                                    'transliteration': None
                               })
    
    def test_bad_nondelimited_search(self):
        '''
        Passes if a request for a nondelimited word that isn't in the database returns a 404 response.
        '''
        response = self.client.get(self.nondelimited_url + "term_not_in_DB", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
