from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
import json

from .models import Definitions



class TestViews(APITestCase):

    text = "hello"
    valid_lang = "en-US"
    invalid_lang = "blah-lang"
    url_one_word = "/api/0.1/search/en-US/hello"
    url_nondelimited_word = "/api/0.1/search/zh-Hant/kool-aidxxxx"
    definition = "A greeting"

    def setUp(self):
        Definitions.objects.create(word_character=self.text,
                                           definition=self.definition)
        Definitions.objects.create(word_character='kool-aid',
                                   definition='the koolest drink ever')

    def test_search_status_code_200(self):
        response = self.client.get(self.url_one_word, format='json')
        self.assertEqual(response.status_code, 200)

    def test_term_search(self):
        response = self.client.get(self.url_one_word, format='json')
        json = response.json()
        self.assertEqual(json, {'word_character': self.text,
                                    'definition': self.definition,
                                    'transliteration': None })

    def test_nondelimited_term_search(self):
        response = self.client.get(self.url_nondelimited_word, format='json')
        json = response.json()
        self.assertEqual(json, {'word_character': 'kool-aid',
                                    'definition': 'the koolest drink ever',
                                    'transliteration': None
                               })

    def test_display(self):
        print('\n\n')
        response = self.client.get(self.url_nondelimited_word, format='json')
        json = response.json()
        print('GET ' + self.url_nondelimited_word)
        print('response:   ' + str(json))
        print('\n\n')
        response = self.client.get(self.url_one_word, format='json')
        json = response.json()
        print('GET ' + self.url_one_word)
        print('response:   ' + str(json))
        print('\n\n')
