from django.core.urlresolvers import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from .serializers import DefinitionSerializer
from rest_framework.renderers import JSONRenderer
import json

from .views import Search
from .models import Definitions


class TestDefinition(object):

    def __init__(self, term, definition, language):
        self.term = term
        self.definition = definition
        self.locale = language


class TestViews(APITestCase):

    text = "hello"
    invalid_language = "blah-lang"
    url = "/api/0.1/search/en-US/hello"
    definition = "A greeting"

    def setUp(self):
        entry = Definitions.objects.create(text=self.text,
                                           language="zh-Hant",
                                           definition=self.definition)

        self.factory = APIRequestFactory()

    def test_search_status_code_200(self):
        request = self.factory.get(reverse('search'), {'text': self.text,
                                                       'language': 'zh-Hant'},
                                   format='json')
        response = Search.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_term_search(self):
        '''
        json_dict = {'text': self.text,
                     'definition': self.definition,
                     'language': 'zh-Hant'}
        request = self.factory.get(reverse('search'), {'text': self.text,
                                                       'language': 'zh-Hant'},
                                   format='json')
        '''

        request = self.factory.get(self.url),
        view = Search.as_view()
        response = view(request)
        response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data[0],
                         json_dict,
                         "Response content is the correct definition, "
                         "text, and language")
