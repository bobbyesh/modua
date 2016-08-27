import json
from rest_framework.test import APITestCase, APIRequestFactory

from .models import Definition, User, Language
from .views import DefinitionGenericView, LanguageWordlistView, LanguageListView

import pdb



class TestViews(APITestCase):


    def setUp(self):
        pass

    def test_language_list_view(self):
        '''
        Tests that the LanguageListView returns all existing languages.
        '''
        Language.objects.create(language='en')

        factory = APIRequestFactory()
        request = factory.get('/api/0.1/languages/', format='json')

        view = LanguageListView.as_view()
        response = view(request)
        lang = response.data[0]
        self.assertDictEqual({'language': 'en'}, lang)

    def test_language_wordlist_view(self):
        '''
        Tests that the wordlist view returns all the dictionary entries for a given language.
        '''
        lang = Language.objects.create(language='en')
        word = Definition.objects.create(word='dude', definition='godly saying', transliteration=None,
                                          language=lang)
        Definition.objects.create(word="hello", definition="A greeting", 
                                          language=lang)

        factory = APIRequestFactory()
        request = factory.get('/api/0.1/languages/en/', format='json')

        view = LanguageWordlistView().as_view()
        response = view(request, language='en')

        test_results = sorted(
                [
                  {
                      'word': 'hello', 
                      'definition': 'A greeting',
                      'transliteration': None 
                  },
                  {
                      'word': 'dude', 
                      'definition': 'godly saying',
                      'transliteration': None 
                  }
                ],
            key=lambda t:t['word']
        )

        responses = sorted([response.data[0], response.data[1]], key=lambda t: t['word'])

        for test, resp in zip(test_results, responses):
            self.assertDictEqual(test, resp)

    def test_searchview(self):
        lang = Language.objects.create(language='en')
        Definition.objects.create(word='dude', definition='godly saying', transliteration=None,
                                          language=lang)
        factory = APIRequestFactory()
        request = factory.get('/api/0.1/languages/en/dude', format='json')
        dude = {
                   'word': 'dude',
                   'definition': 'godly saying',
                   'transliteration': None
               }
        view = DefinitionGenericView.as_view()
        response = view(request, language='en', word='dude')
        self.assertDictEqual(dude, response.data[0])

    def test_searchview_no_term(self):
        lang = Language.objects.create(language='en')
        Definition.objects.create(word='dude', definition='godly saying', transliteration=None,
                                          language=lang)
        factory = APIRequestFactory()
        request = factory.get('/api/0.1/languages/en/no_term', format='json')
        dude = {
                   'word': 'meek',
                   'definition': 'godly saying',
                   'transliteration': None
               }
        view = DefinitionGenericView.as_view()
        response = view(request, language='en', word='no_term')
        self.assertEqual(response.status_code, 404)
