from django.test import TestCase
from api.filters import WordFilter
from api.models import Word, Language


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

