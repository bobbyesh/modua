# test_urls.py
from django.test import TestCase
from django.core.urlresolvers import reverse, resolve


class URLReverseTestCase(TestCase):

    def test_root(self):
        url = reverse('api-root')
        self.assertEqual(url, '/api/0.1/')

    def test_definition_detail(self):
        url = reverse('definition-detail', kwargs={'language':'en', 'word':'foo', 'id':'1'})
        self.assertEqual(url, '/api/0.1/languages/en/foo/1/')

    def test_language_list(self):
        url = reverse('language-list')
        self.assertEqual(url, '/api/0.1/languages/')

    def test_language_word_list(self):
        url = reverse('language-definitions', kwargs={'language': 'en'})
        self.assertEqual(url, '/api/0.1/languages/en/')


class URLResolveTestCase(TestCase):

    def test_root(self):
        resolver = resolve('/api/0.1/')
        self.assertEqual(resolver.view_name, 'api-root')

    def test_definition_detail(self):
        resolver = resolve('/api/0.1/languages/en/foo/1/')
        self.assertEqual(resolver.view_name, 'definition-detail')

    def test_language_list(self):
        resolver = resolve('/api/0.1/languages/')
        self.assertEqual(resolver.view_name, 'language-list')

    def test_language_word_list(self):
        resolver = resolve('/api/0.1/languages/en/')
        self.assertEqual(resolver.view_name, 'language-definitions')
