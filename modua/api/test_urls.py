# test_urls.py
from django.test import TestCase
from django.core.urlresolvers import reverse, resolve


class URLReverseTestCase(TestCase):

    def test_root(self):
        url = reverse('api:api-root')
        self.assertEqual(url, '/api/')
