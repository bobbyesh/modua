from django.test import TestCase
from api.filters import WordFilter, DefinitionFilter
from api.models import Word, Language, Definition
from django.contrib.auth.models import User


class WordFilterTestCase(TestCase):

    def setUp(self):
        Language.objects.create(language='en')
        Language.objects.create(language='es')
        Language.objects.create(language='zh')
        Word.create('hey', 'en').add_definition('hola', 'es')

    def test_filter(self):
        queryset = Word.objects.all()
        params = {'language': 'zh', 'word': 'not_in_db'}
        filtered = WordFilter(params, queryset=queryset).qs
        self.assertQuerysetEqual(filtered, [])

    def test_filter_good(self):
        queryset = Word.objects.all()
        params = {'language': 'en', 'word': 'hey'}
        filtered = WordFilter(params, queryset=queryset).qs
        self.assertTrue(filtered != [])


class DefinitionFilterTestCase(TestCase):

    def setUp(self):
        self.john = User.objects.create(username='john', password='password')
        Language.objects.create(language='en')
        self.es = Language.objects.create(language='es')
        Language.objects.create(language='zh')
        Word.create('hey', 'en').add_definition('hola', 'es')

    def test_filter_empty(self):
        queryset = Definition.objects.all()
        params = {'language': 'zh', 'word': 'not_in_db'}
        filtered = DefinitionFilter(params, queryset=queryset).qs
        self.assertQuerysetEqual(filtered, [])

    def test_filter_match(self):
        queryset = Definition.objects.all()
        params = {'word': 'hey', 'target': 'es'}
        filtered = DefinitionFilter(params, queryset=queryset).qs
        expected = Definition.objects.filter(word__word='hey', language__language='es')
        self.assertEqual(filtered[0], expected[0])

    def test_filter_mismatch_target_language(self):
        queryset = Definition.objects.all()
        params = {'word': 'hey', 'target': 'zh'}
        filtered = DefinitionFilter(params, queryset=queryset).qs
        self.assertQuerysetEqual(filtered, [])

    def test_filter_by_user(self):
        w = Word.create('no', 'en')
        w.set_user('john')
        queryset = Definition.objects.all()
        Definition.objects.create(definition='spanish no', owner=self.john, word=w, language=self.es)
        params = {'word': 'no', 'language': 'en', 'username': 'john'}
        filtered = DefinitionFilter(params, queryset=queryset).qs[0]
        expected = Definition.objects.filter(word__word='no', word__language__language='en', owner__username='john')[0]
        self.assertEqual(filtered, expected)

