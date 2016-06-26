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
        pass


    def test_language_wordlist_view_only(self):
        '''
        Tests that the wordlist view returns all the dictionary entries for a given language.
        '''
        lang = Languages.objects.create(language='en')
        lang = Languages.objects.get(language='en')
        word = Definitions.objects.create(word_character='dude', definition='godly saying', transliteration=None,
                                          fk_definitionlang=lang)
        Definitions.objects.create(word_character="hello", definition="A greeting", 
                                          fk_definitionlang=lang)

        factory = APIRequestFactory()
        request = factory.get('/api/0.1/language/en/', format='json')

        view = LanguageWordlistView().as_view()
        response = view(request, language='en')

        test_results = sorted(
                [
                  {
                      'word_character': 'hello', 
                      'definition': 'A greeting',
                      'transliteration': None 
                  },
                  {
                      'word_character': 'dude', 
                      'definition': 'godly saying',
                      'transliteration': None 
                  }
                ],
            key=lambda t:t['word_character']
        )

        responses = sorted([response.data[0], response.data[1]], key=lambda t: t['word_character'])

        for test, resp in zip(test_results, responses):
            self.assertDictEqual(test, resp)
