# test_urls.py
from django.test import TestCase
from django.core.urlresolvers import reverse, resolve


class URLReverseTestCase(TestCase):

    def test_root(self):
        url = reverse('api-root')
        self.assertEqual(url, '/api/0.1/')

    def test_language_list(self):
        url = reverse('language-list')
        self.assertEqual(url, '/api/0.1/languages/')


class URLResolveTestCase(TestCase):

    def test_root(self):
        resolver = resolve('/api/0.1/')
        self.assertEqual(resolver.view_name, 'api-root')

    def test_language_list(self):
        resolver = resolve('/api/0.1/languages/')
        self.assertEqual(resolver.view_name, 'language-list')
