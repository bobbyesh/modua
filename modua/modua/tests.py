from django.test import TestCase, Client, RequestFactory
from django.http import JsonResponse
from django.db import models
from modua_app.nondelimited_text import NonDelimitedText


class TestRequests(TestCase):
        
    test_string = "天下無雙"
    test_locale = "zh_HANT"
    test_list = ["天","天下","天下無","天下無雙"]

    def setUp(self):
        '''Setup this test case with a Client and RequestFactory to test views'''
        self.client = Client()
        self.factory = RequestFactory()

    def test_request_successful(self):
        '''Passes if a generic GET request to 'oursite.com/lookup/' returns a
        response with status code 200.
        '''
        response = self.client.get("/lookup/foo")
        self.assertEqual(response.status_code, 200, "/lookup/foo resturns status code 200)")

    
    def get_basic_request(self):
        '''Return a basic request with value pairs: string = test_string and
        locale = test_locale
        '''
        url = self.build_valid_url()
        request = self.factory.get(url)
        return request;
    
    
    def build_valid_url(self):
        '''Returns a string that is a valid GET request and url'''
        string_pair = "string=" + self.test_string
        locale_pair =  "locale=" + self.test_locale
        url = "/lookup/?" + string_pair + "&" + locale_pair
        return url
        



    def test_nondelimited_text_generator(self):
        '''Passes if a list built from the NonDelimitedText's sub_unit property is
        equal to the list it should be equal too, the test_list
        '''
        text = NonDelimitedText(self.test_string, self.test_locale)
        self.assertEqual(list(text.sub_units), self.test_list)

    def test_response_is_JsonResponse(self):
        response = self.client.get(self.build_valid_url())
        self.assertIsInstance(response, JsonResponse)
